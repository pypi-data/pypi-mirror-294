from os import path
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.colors import Normalize, ListedColormap, LinearSegmentedColormap
from matplotlib.quiver import Quiver
import matplotlib.cm
import matplotlib.animation as animation
from matplotlib.path import Path
from matplotlib import _api
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from scipy.spatial import cKDTree, Voronoi, ConvexHull
from shapely.geometry import Polygon as ShapelyPolygon
import warnings
from time import time

from .astroid import gsw_astroid

fs_colours= [      [.9, .1, .1],
                    [.9, .9, .1],
                    [.1, .7, .2],
                    [.1, .7, .9],
                    [.1, .1, .9],
                    [.9, .1 , .9],
                    [.9, .1, .1]]
cmap = LinearSegmentedColormap.from_list('flatspin', fs_colours, N=1000)
matplotlib.colormaps.register(cmap, force=True)
normalize_rad = Normalize(vmin=0, vmax=2*np.pi)

# Colormap from Li et al., (2019)
clist = list('ckkbbkkggkkrrkkc')
clist = ['#00da00' if c == 'g' else c for c in clist]
clist = ['#0800da' if c == 'b' else c for c in clist]
clist = ['#ed0912' if c == 'r' else c for c in clist]
clist = ['#00ccff' if c == 'c' else c for c in clist]

cmap = ListedColormap(clist, 'li2019')
matplotlib.colormaps.register(cmap, force=True)

# Type 1: green, type 2: blue, type 3: red, type 4: gray
clist = [(.1, .7, .2), (.1, .1, .9), (.9, .1, .1), (.4,.4,.4)]
cmap = ListedColormap(clist, 'vertex-type')
matplotlib.colormaps.register(cmap, force=True)

def quadrilaterals(X):
    dX = X[1:]-X[:-1]
    dX = np.pad(dX, 1, mode='edge')
    dX[:-1] *= -1 # subtract dX/2 from all but last element, where we add dX/2
    # quads needs one more value (see pcolormesh)
    quads = np.pad(X, (0,1), mode='edge').astype(float)
    quads += dX/2
    return quads

def format_label(label, format_spec='{:g}'):
    if isinstance(label, tuple):
        lbl = ', '.join(map(format_label, label))
        return f'({lbl})'

    if isinstance(label, list):
        return ', '.join(map(format_label, label))

    try:
        return format_spec.format(label)
    except:
        return str(label)

def format_labels(labels, format_spec='{:g}'):
    return [format_label(l, format_spec) for l in labels]

def heatmap2(X, Y, Z, xlabel='x', ylabel='y', zlabel='z', xlabels=None, ylabels=None, **kwargs):
    X = np.array(X)
    Y = np.array(Y)
    Z = np.array(Z)
    print(X.shape, Y.shape, Z.shape)
    print(X.dtype, Y.dtype, Z.dtype)

    if not xlabels:
        xlabels = format_labels(X)

    #if X.dtype == object:
    #    X = np.arange(len(X))

    if not ylabels:
        ylabels = format_labels(Y)

    #if Y.dtype == object:
    #    Y = np.arange(len(Y))

    Xi = np.arange(len(X))
    Yi = np.arange(len(Y))
    print(Yi)
    qX = quadrilaterals(Xi)
    qY = quadrilaterals(Yi)

    def format_coord(x, y):
        # find nearest x,y
        #idx = np.abs(x-Xi).argmin()
        #idy = np.abs(y-Yi).argmin()
        idx = int(x + 0.5)
        idy = int(y + 0.5)
        x = xlabels[idx]
        y = ylabels[idy]
        z = Z[idy, idx]
        return f'{xlabel}={x}, {ylabel}={y}, {zlabel}={z:g}'

    ax = plt.gca()
    ax.format_coord = format_coord
    ax.xaxis.set_major_locator(ticker.FixedLocator(Xi, nbins=min(len(Xi), 10)))
    ax.yaxis.set_major_locator(ticker.FixedLocator(Yi, nbins=min(len(Yi), 10)))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter((lambda x,pos: xlabels[x])))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter((lambda y,pos: ylabels[y])))
    #ax.xaxis.set_major_formatter(ticker.FuncFormatter((lambda x,pos: (x,pos))))
    #ax.yaxis.set_major_formatter(ticker.FuncFormatter((lambda y,pos: (y,pos))))
    #ax.set_xticklabels(xlabels)
    #ax.set_yticklabels(ylabels)
    return plt.pcolormesh(qX, qY, Z, **kwargs)

def heatmap(X, Y, Z, xlabel='x', ylabel='y', zlabel='z',
        xlim=None, ylim=None, zlim=None, nticks=10,
        xlabel_format='{:g}', ylabel_format='{:g}',
        ax=None,
        **kwargs):

    xlabels = format_labels(X, xlabel_format)
    ylabels = format_labels(Y, ylabel_format)

    X = np.array(X)
    Y = np.array(Y)
    Z = np.array(Z)

    Xi = np.arange(len(X))
    Yi = np.arange(len(Y))

    def format_coord(x, y):
        try:
            idx = int(x)
            idy = int(y)
            x = xlabels[idx]
            y = ylabels[idy]
            z = Z[idy, idx]
            return f'{xlabel}={x}, {ylabel}={y}, {zlabel}={z:g}'
        except IndexError:
            return ''

    if ax is None:
        ax = plt.gca()

    ax.format_coord = format_coord
    nbins = min(len(Xi), nticks) if X.dtype != 'object' else None
    ax.xaxis.set_major_locator(ticker.FixedLocator(Xi+.5, nbins=nbins))
    nbins = min(len(Yi), nticks) if Y.dtype != 'object' else None
    ax.yaxis.set_major_locator(ticker.FixedLocator(Yi+.5, nbins=nbins))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter((lambda x,pos: xlabels[int(x)])))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter((lambda y,pos: ylabels[int(y)])))

    if zlim:
        kwargs['vmin'], kwargs['vmax'] = zlim

    pcolor = ax.pcolormesh(Z, **kwargs)

    # We have integer indexes on the axes, so need to map x values to x indexes
    if xlim and X.dtype != 'object':
        xmin, xmax = xlim
        ximin = np.argmax(X >= xmin)
        ximax = np.argmax(X > xmax)
        ax.set_xlim(ximin, ximax)

    if ylim and Y.dtype != 'object':
        ymin, ymax = ylim
        yimin = np.argmax(Y >= ymin)
        yimax = np.argmax(Y > ymax)
        ax.set_ylim(yimin, yimax)

    return pcolor

def vector_angle(U, V):
    C = np.arctan2(V, U) # color
    C[C<0] = 2*np.pi + C[C<0]
    return C

def vector_rgba(U,V, mag_max=1, cmap='hsv'):
    ''' Return rgba values according to color map and normalized vector
    magnitude.
    '''
    # base color from vector angle and cmap
    angle = vector_angle(U, V)
    mapper = matplotlib.cm.ScalarMappable(norm=normalize_rad, cmap=plt.get_cmap(cmap))
    rgba = mapper.to_rgba(angle)
    # normalize magnitude
    mag = norm([U,V], axis=0) / mag_max
    # adjust alpha according to normalized magnitude
    rgba[:,-1] *= mag

    return rgba

def mask_zero_vectors(UV):
    # mask out zero vectors
    mag = norm(UV, axis=-1)
    mask = np.repeat(mag <= 1e-12, 2).reshape(UV.shape)
    return np.ma.array(UV, mask=mask)

class SpinQuiver(Quiver):
    """ Custom Quiver with support for different spin styles (shapes) """

    def __init__(self, *args, style="arrow", **kwargs):
        assert style in ("arrow", "rectangle", "stadium")
        self.style = style
        super().__init__(*args, **kwargs)

    def _h_arrows(self, length):
        # let Quiver handle the "arrow" style
        if self.style == "arrow":
            return super()._h_arrows(length)

        # modified from Quiver._h_arrows()
        N = len(length)
        length = length.reshape(N, 1)

        # This number is chosen based on when pixel values overflow in Agg
        # causing rendering errors
        # length = np.minimum(length, 2 ** 16)
        np.clip(length, 0, 2 ** 16, out=length)

        # Draw a rectangle
        X = np.array([0, 0, 1, 1, 0], np.float64) * length
        Y = np.array([0, 1, 1, 0, 0], np.float64) - 0.5
        Y = np.repeat(Y[np.newaxis, :], N, axis=0)

        if self.pivot == 'middle':
            X -= 0.5 * X[:, 3, np.newaxis]
        elif self.pivot == 'tip':
            # numpy bug? using -= does not work here unless we multiply by a
            # float first, as with 'mid'.
            X = X - X[:, 3, np.newaxis]
        elif self.pivot != 'tail':
            _api.check_in_list(["middle", "tip", "tail"], pivot=self.pivot)

        tooshort = length < self.minlength
        if tooshort.any():
            # Use a square
            tooshort = tooshort.ravel()
            X[tooshort] = np.array([-1, 0, 1, 0, -1]) * self.minlength * 0.5
            Y[tooshort] = np.array([ 0, 1, 0, -1, 0]) * self.minlength * 0.5

        # Mask handling is deferred to the caller, _make_verts.
        return X, Y

    def set_verts(self, verts, closed=True):
        # The drawn Paths are created in set_verts().
        # We override this to create paths for stadium shape.
        if self.style != "stadium":
            return super().set_verts(verts, closed)

        if len(verts) == 0:
            return

        verts = np.array(verts)
        assert verts.shape[1] == 5

        codes = [Path.MOVETO,
                 Path.CURVE4,
                 Path.CURVE4,
                 Path.CURVE4,
                 Path.LINETO,
                 Path.CURVE4,
                 Path.CURVE4,
                 Path.CURVE4,
                 Path.LINETO]

        # New vertices for the path
        new_verts = np.empty((len(verts), len(codes), 2))

        # Create left bezier curve
        v1 = .7 * (verts[:,1] - verts[:,0])
        # n1 is v1 rotated by 90 degrees
        n1 = np.column_stack([-v1[:,1], v1[:,0]])

        # First and second control points
        new_verts[:,1] = verts[:,0] + .25*n1
        new_verts[:,2] = verts[:,1] + .25*n1

        # Move original vertices back to accomodate curve
        new_verts[:,0] = verts[:,0] - .75*n1
        new_verts[:,3] = verts[:,1] - .75*n1

        # Create right bezier curve in similar fashin
        v2 = .7 * (verts[:,3] - verts[:,2])
        n2 = np.column_stack([-v2[:,1], v2[:,0]])
        new_verts[:,5] = verts[:,2] + .25*n2
        new_verts[:,6] = verts[:,3] + .25*n2
        new_verts[:,4] = verts[:,2] - .75*n2
        new_verts[:,7] = verts[:,3] - .75*n2

        # Close the path
        new_verts[:,8] = new_verts[:,0]

        # Create path objects
        self._paths = [Path(xy, codes) for xy in new_verts]


def spin_quiver(*args, ax=None, **kwargs):
    # Identical to ax.quiver(), but for SpinQuiver
    ax = ax or plt.gca()
    args = ax._quiver_units(args, kwargs)
    q = SpinQuiver(ax, *args, **kwargs)
    ax.add_collection(q, autolim=True)
    ax._request_autoscale_view()
    return q

def plot_vectors(XY, UV, C=None, style="arrow", mask_zero=True, replace=False,
        normalize=False, ax=None, set_ax_lims=True,
        dir_only=False, alpha_mag=False, **kwargs):

    if 'arrows' in kwargs:
        # Maintain backwards compatibility with old arrows=True/False
        warnings.warn('arrows is deprecated, use style="arrow" instead.',
                DeprecationWarning)
        arrows = kwargs.pop('arrows')
        style = "arrow" if arrows else "rectangle"

    XY = np.atleast_2d(XY)
    UV = np.atleast_2d(UV)
    XY = XY.reshape((-1, 2)) # quiver wants 2D XY
    X = XY[...,0] # x components
    Y = XY[...,1] # y components

    if normalize:
        # Normalize vectors to unit length
        nmax = norm(UV.reshape((-1,2)), axis=-1).max()
        if nmax != 0:
            UV = UV / nmax

    if alpha_mag:
        # Use alpha channel for magnitude
        norms = norm(UV, axis=-1).ravel()
        alpha = norms / np.max(norms)
        kwargs.setdefault('alpha', alpha)

    if dir_only:
        # Plot vector directions only
        norms = norm(UV, axis=-1)
        UV = UV / np.expand_dims(norms, -1)

    if mask_zero:
        UV = mask_zero_vectors(UV)

    U = UV[..., 0] # x components
    V = UV[..., 1] # y components
    if C is None:
        C = vector_angle(U, V)
        kwargs.setdefault('norm', normalize_rad)

    if ax is None:
        ax = plt.gca()

    if replace and len(ax.collections) > 0:
        quiv = ax.collections[0]
        old_XY = quiv.get_offsets()
        if not np.array_equal(old_XY, XY):
            # Positions have changed, create a new quiver
            replace = False
            quiv.remove()

    if replace and len(ax.collections) > 0:
        # Replace current quiver data
        quiv = ax.collections[0]
        quiv.set_UVC(U, V, C)
        if 'alpha' in kwargs:
            quiv.set_alpha(kwargs['alpha'])

    else:
        # Make a new quiver

        # Determine scale based on the average distance between nearest neighbors
        tree = cKDTree(XY)
        min_dist = np.mean(tree.query(XY, k=[2])[0])
        scale = 1.15/min_dist if not np.isinf(min_dist) and min_dist != 0 else 1

        kwargs.setdefault('cmap', 'flatspin')
        kwargs.setdefault('scale', scale)
        kwargs.setdefault('pivot', 'middle')
        if style == "arrow":
            kwargs.setdefault('width', 0.2/scale)
            kwargs.setdefault('headwidth', 3)
            kwargs.setdefault('headlength', 2)
            kwargs.setdefault('headaxislength', 2)
        else:
            # rectangle / stadium
            kwargs.setdefault('width', 0.3/scale)
            kwargs.setdefault('headwidth', 0)
            kwargs.setdefault('headlength', 0)
            kwargs.setdefault('headaxislength', 0)

        if type(kwargs["cmap"]) is str and kwargs["cmap"].startswith("peem"):
            # clever peem colormap
            peem_angle = np.deg2rad(float(kwargs["cmap"].strip("peem")))
            intensity = np.cos(np.linspace(0, 2 * np.pi, 360) - peem_angle)
            intensity = intensity * 0.5 + 0.5  # scale from (-1,1) to (0,1)
            intensity = np.tile(intensity, (3, 1)).T  # [[0],...,[1]] -> [[0,0,0],...,[1,1,1]]
            kwargs["cmap"] = ListedColormap(intensity)
            ax.set_facecolor([0.5] * 3)

        # If user passed in explicit colors (via the 'color' kwarg) we omit C
        # from args, since quiver doesn't allow C to be passed as kwarg.
        args = [X, Y, U, V]
        if 'color' not in kwargs:
            args.append(C)
        quiv = spin_quiver(*args, ax=ax, style=style, units='xy',
                angles='xy', scale_units='xy', **kwargs)

        ax.set_aspect('equal')

        # Make space for the whole arrow
        if set_ax_lims:
            xmin, xmax = np.min(X), np.max(X)
            ymin, ymax = np.min(Y), np.max(Y)
            ax.set_xlim(xmin - 1/scale, xmax + 1/scale)
            ax.set_ylim(ymin - 1/scale, ymax + 1/scale)

    return quiv

def get_voronoi_polys(XY, bounding_hull=None):
    # Create the Voronoi object
    vor = Voronoi(np.asarray(XY))
    # Create the bounding shape
    bounding_hull = ConvexHull(bounding_hull) if bounding_hull is not None else ConvexHull(np.asarray(XY))
    # Create a Path object for the ConvexHull for easy point-in-polygon checks
    bounding_hull_path = Path(bounding_hull.points[bounding_hull.vertices])
    # Create a Shapely Polygon of the bounding_hull
    bounding_hull_shapely = ShapelyPolygon(bounding_hull.points[bounding_hull.vertices])

    XY_center = vor.points.mean(axis=0)
    XY_bound = vor.points.ptp(axis=0)

    # Store all polygons in an array
    polys = []
    # Create every region as a Polygon
    for point_idx, region_idx in enumerate(vor.point_region):
        region = np.asarray(vor.regions[region_idx])
        if len(region) == 0:
            continue
        if np.ma.is_masked(XY[point_idx]):
            polys.append([(0,0)])
            continue

        # Add vertices that are not at infinity
        vertices = vor.vertices[region[region>=0]]

        if -1 in region:  # Unbounded region
            # add far_point as in https://github.com/scipy/scipy/blob/v1.11.2/scipy/spatial/_plotutils.py#L232-L265
            # Find ridges defining the region of this point
            ridges = np.where((vor.ridge_points == point_idx).any(axis=1))[0]

            # Loop through ridges of the point
            for ridge_idx in ridges:
                ridge_vert = vor.ridge_vertices[ridge_idx]
                if -1 in ridge_vert:  # The ridge has a point at infinity, and we need to add a far point

                    finite_vertex = [v for v in ridge_vert if v != -1][0]  # finite vertex
                    neighbor_points = vor.ridge_points[ridge_idx] # the points that the ridge lies between

                    t = vor.points[neighbor_points[1]] - vor.points[neighbor_points[0]]  # tangent
                    t /= np.linalg.norm(t)
                    n = np.array([-t[1], t[0]])  # normal

                    midpoint = vor.points[neighbor_points].mean(axis=0)
                    direction = np.sign(np.dot(midpoint - XY_center, n)) * n

                    if (vor.furthest_site):
                        direction = -direction

                    far_point = vor.vertices[finite_vertex] + direction * XY_bound.max()
                    # Use far_point as a new vertex of the region
                    vertices = np.concatenate([vertices,far_point.reshape(1,2)])

        # (Bounded region straightforwardly includes all vertices)
        # Turn vertices into convex hull to avoid self-intersection etc.
        region_hull = ConvexHull(vertices)
        poly = region_hull.points[region_hull.vertices]
        clip_path = Path(poly)

        if bounding_hull_path.contains_path(clip_path):
            # Completely inside bounding hull
            polys.append(poly)
        else:
            # Clipped by hull, compute clipped poly
            poly_shapely = ShapelyPolygon(poly)
            clipped_poly = poly_shapely.intersection(bounding_hull_shapely)
            if clipped_poly.is_empty:
                raise ValueError('Bounding hull does not contain voronoi region')
                continue

            poly = list(zip(*clipped_poly.exterior.xy))
            polys.append(poly)

    return polys

def plot_voronoi(XY, UV, bounding_hull=None, alpha=1.0, arrows=False, mask_zero=True, edgecolor='none', replace=False, ax=None,
         **kwargs):
    if mask_zero:
        UV = mask_zero_vectors(UV)
        XY = np.ma.array(XY, mask=UV.mask)

    # components
    X = XY[...,0]
    Y = XY[...,1]
    U = UV[..., 0]
    V = UV[..., 1]

    # Set colors by vector_rgba if colors is not specified
    if kwargs.get('colors', None) is not None:
        colors = kwargs['colors']
    else:
        colors = vector_rgba(U, V, mag_max=np.max(norm(UV,axis=-1)), cmap=kwargs.get('cmap', 'flatspin'))
    if len(np.atleast_1d(alpha)) == 1:
        # If 1 alpha value is provided, scale magnitude by that value to set alpha
        colors[:,-1] *= alpha
    else:
        # Set alpha explicitly
        assert len(alpha) == len(UV)
        colors[:,-1] = alpha

    # Validate edgecolor
    if isinstance(edgecolor, str):
        edgecolors = [edgecolor] * len(XY)
    elif isinstance(edgecolor, (list, np.ndarray)):
        assert len(edgecolor) == len(XY)
        edgecolors = edgecolor
    else:
        raise TypeError("Unsupported type for edgecolor")

    polys = get_voronoi_polys(XY, bounding_hull=bounding_hull)
    patches = [Polygon(poly, facecolor=color, edgecolor=ec) for poly, color, ec in zip(polys, colors, edgecolors)]
    p = PatchCollection(patches, match_original=True)

    if ax is None:
        ax = plt.gca()
    ax.add_collection(p)

    # TODO: implement replace behavior
    if replace:
        raise NotImplementedError

    ax.set_aspect('equal')
    # Crop to XY values
    if kwargs.get('set_ax_lims', True):
        xmin, xmax = np.min(X), np.max(X)
        ymin, ymax = np.min(Y), np.max(Y)
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)

    # plot_vectors() will overwrite crop (unless set_ax_lims is False)
    if arrows:
        plot_vectors(XY, UV, normalize=True, mask_zero=mask_zero, replace=replace, ax=ax,**kwargs)

    return ax

def plot_vector_image(XY, UV, mask_zero=True, replace=False, cmap='flatspin', ax=None):
    if mask_zero:
        UV = mask_zero_vectors(UV)

    U = UV[...,0] # x components
    V = UV[...,1] # y components
    C = vector_angle(U, V)

    cmap = plt.get_cmap(cmap)
    mag = norm(UV, axis=-1)
    alpha = mag

    # print(f'alpha {np.min(alpha)} {np.max(alpha)}')
    im = cmap(normalize_rad(C))
    im[:,:,-1] = alpha
    # print(f'im {im.shape} {im}')

    if ax is None:
        ax = plt.gca()


    if replace and len(ax.images) > 0:
        # Replace current image data
        ax.images[0].set_data(im)
        return ax.images[0]

    X = np.unique(XY[..., 0]) # x components
    Y = np.unique(XY[..., 1]) # y components
    Xi = np.arange(len(X))
    Yi = np.arange(len(Y))

    xmin, xmax = X.min(), X.max()
    ymin, ymax = Y.min(), Y.max()

    def format_coord(x, y):
        x = xmin + (xmax-xmin) * x / (im.shape[1] - 1)
        y = ymin + (ymax-ymin) * y / (im.shape[0] - 1)
        return f'x={x:g}, y={y:g}'

    ax.format_coord = format_coord
    nbins = min(len(Xi), 10)
    ax.xaxis.set_major_locator(ticker.FixedLocator(Xi, nbins=nbins))
    nbins = min(len(Yi), 10)
    ax.yaxis.set_major_locator(ticker.FixedLocator(Yi, nbins=nbins))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter((lambda x,pos: "{:g}".format(X[int(x)]))))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter((lambda y,pos: "{:g}".format(Y[int(y)]))))

    return ax.imshow(im, origin='lower')

def montage_fig(n_axes, title=False):
    """ Create a figure with n_axes subplots on a grid """
    n_rows = int(np.ceil(np.sqrt(n_axes)))
    n_cols = int(np.ceil(n_axes / n_rows))
    gs = dict(wspace=0.05, hspace=0.25, left=0.05, right=0.95, top=0.95, bottom=0.05)
    figsize = [6.4, 6.4]

    if title:
        gs.update(top=0.85) # todo: fixme

    fig, axes = plt.subplots(n_rows, n_cols, gridspec_kw=gs, figsize=figsize, squeeze=False)
    axes = axes.flatten()

    for ax in axes:
        ax.tick_params(
            top=False, bottom=False, left=False, right=False,
            labeltop=False, labelbottom=False, labelleft=False, labelright=False)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        ax.grid(False)

    # hide unused axes
    for ax in axes[n_axes:]:
        ax.set_visible(False)

    return fig, axes

def vector_montage(axes, positions, vectors, labels=None, style="image", **kwargs):
    for i, (XY, UV, ax) in enumerate(zip(positions, vectors, axes)):
        if style == "image":
            kwargs.pop("dir_only", None) # unused params for style==image
            kwargs.pop("alpha_mag", None)
            plot_vector_image(XY, UV, replace=True, ax=ax, **kwargs)
        else:
            plot_vectors(XY, UV, style=style, replace=True, ax=ax, **kwargs)

        if labels:
            ax.set_title(labels[i], size='x-small', pad=2)

def save_animation(ani, outfile, fps=30, dpi=100):
    base, ext = path.splitext(outfile)
    ext = ext.lstrip('.')

    if ext == 'mp4':
        print(f"Saving video {outfile}...")
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=fps, codec='h264', extra_args=['-crf', '0', '-g', '1'])
        ani.save(outfile, writer=writer, dpi=dpi)
        return

    if ext in animation.writers['imagemagick_file'].supported_formats:
        print(f"Saving image(s) {outfile}...")
        Writer = animation.writers['imagemagick_file']
        # extra_args=[] is a workaround for matplotlib #24268
        writer = Writer(fps=fps, extra_args=[])
        ani.save(outfile, writer=writer, dpi=dpi)
        return

    if ext == 'gif':
        print(f"Saving GIF {outfile}...")
        Writer = animation.writers['imagemagick']
        writer = Writer(fps=fps)
        ani.save(outfile, writer=writer, dpi=dpi)
        return

    raise ValueError(f"Don't know how to write '{ext}', sorry")

class FuncAnimationCtrl(animation.FuncAnimation):
    """ FuncAnimation with key controls to control playback """
    def __init__(self, fig, func, frames, **kwargs):
        self.paused = False
        self.direction = 1
        self._frame_seq_started = False

        if not np.iterable(frames):
            frames = np.arange(frames)
        self.frames = frames

        super().__init__(fig, func, frames=self.frame_iter, **kwargs)

        fig.canvas.mpl_connect('key_press_event', self.on_press)

    def frame_iter(self):
        n_frames = len(self.frames)
        i = 0 if self.direction == 1 else (n_frames - 1)
        while 0 <= i < n_frames:
            yield self.frames[i]
            i += self.direction
            self._frame_seq_started = True

    def pause(self):
        if self.event_source:
            super().pause()
        self.paused = True

    def resume(self):
        if self.event_source is None:
            return
        super().resume()
        self.paused = False

    def new_frame_seq(self):
        self._frame_seq_started = False
        return super().new_frame_seq()

    def step(self):
        self._step()
        if not self._frame_seq_started:
            # Finished the sequence, _step() has created a new frame_seq and
            # would normally trigger an extra draw step through the event source
            self._step()

    def on_press(self, event):
        if event.key == ' ':
            self.direction = 1
            if self.paused:
                self.resume()
            else:
                self.pause()
            return

        if event.key == 'down':
            self.direction = 1
        elif event.key == 'up':
            self.direction = -1

        if event.key in ('down', 'up'):
            if self.paused:
                self.step()
            else:
                self.pause()

def plot_h_ext(h_ext):
    h_ext = np.array(h_ext)

    # (time, 2): a global vector signal
    # (time, H, W, 2): a local vector signal on a grid
    assert h_ext.ndim == 2 or h_ext.ndim == 4

    if h_ext.ndim == 2:
        # (time, 2): a global vector signal
        plt.plot(h_ext[:,0], label="x")
        plt.plot(h_ext[:,1], label="y")
        plt.xlabel('t')
        plt.ylabel('h_ext')
        plt.legend()

    elif h_ext.ndim == 4:
        # (time, H, W, 2): a local vector signal on a grid
        nrows = h_ext.shape[1]
        ncols = h_ext.shape[2]
        fig = plt.gcf()
        axes = fig.subplots(nrows, ncols, squeeze=False, sharex=True, sharey=True)
        for row, col in np.ndindex((nrows, ncols)):
            ax = axes[row, col]
            j = nrows - row - 1
            i = col
            ax.text(.95, .95, f"({j},{i})", horizontalalignment='right',
                    verticalalignment='top', transform=ax.transAxes,
                    zorder=0)
            ax.plot(h_ext[:,j,i,0], label="x")
            ax.plot(h_ext[:,j,i,1], label="y")
            if i == 0:
                ax.set_ylabel('h_ext')
            else:
                ax.tick_params('y', labelleft=False)
            if j == 0:
                ax.set_xlabel('t')
            else:
                ax.tick_params('x', labelbottom=False)
            if (j, i) == (nrows - 1, ncols - 1):
                ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.05))
        plt.subplots_adjust(wspace=0, hspace=0)

def gridless_crop(x, crop_percent):
    """ Return the indices of x that are inside the crop """
    minx, maxx = np.min(x[:,0]), np.max(x[:,0])
    miny, maxy = np.min(x[:,1]), np.max(x[:,1])
    crop_width = ((np.array(crop_percent)/100).T * [maxy - miny, maxx - minx]).T
    return np.logical_and(
                np.logical_and(
                    x[:,0] >= minx + crop_width[1][0],
                    x[:,0] <= maxx - crop_width[1][1]
                ),
                np.logical_and(
                    x[:,1] >= miny + crop_width[0][0],
                    x[:,1] <= maxy - crop_width[0][1]
                )
    )

def plot_astroid(b=1, c=1, beta=3, gamma=3, hc=1, rotation=0, resolution=361,
        angle_range=(0, 2*np.pi), ax=None, **kwargs):

    astroid = gsw_astroid(b, c, beta, gamma, hc, rotation, resolution, angle_range)
    h_par, h_perp = astroid.T

    if ax is None:
        ax = plt.gca()

    ax.set_aspect('equal')

    return ax.plot(h_par, h_perp, **kwargs)

def plot_color_wheel(angles=8, angle_start=0, angle_range=360, radians=False,
        center_radius=0.13, center_color='white', ax=None, **kwargs):

    if np.isscalar(angles):
        angle_stop = angle_start + angle_range
        angles = np.arange(angle_start, angle_stop, (angle_stop - angle_start) / angles)

    if not radians:
        angles = np.radians(angles)

    ax = ax or plt.gca()

    circle = plt.Circle([0, 0], radius=center_radius, fc=center_color, zorder=100)
    ax.add_patch(circle)

    XY = np.zeros((len(angles), 2))
    UV = np.column_stack([np.cos(angles), np.sin(angles)])

    kwargs.setdefault('width', .1)

    return plot_vectors(XY, UV, pivot='tail', ax=ax, **kwargs)
