#pragma OPENCL EXTENSION cl_khr_fp64 : enable

int d2_to_d1(int x, int y, int nx) {
    return x * nx + y;
}

double2 external_field(
    int i,
    __global char * spin,
    __global double2 * m,
    __global double2 * h_ext)
{
    double2 mi = spin[i] * m[i];
    double2 mi_perp = {-mi.y, mi.x};
    double h_par = dot(h_ext[i], mi);
    double h_perp = dot(h_ext[i], mi_perp);

    return (double2)(h_par, h_perp);
}

double2 h_dip_local(
    int i,
    __global char * spin,
    __global double2 * h_dip_cache,
    double alpha,
    __global int * neighbors,
    int n_neighbors)
{
    double2 h_dip = {0, 0};

    //all neighbors

    //h_dip_cache is a 2d array index on (spin, neighbor) = <num>
    //same with neighbors-array
    //iterate neighbors
    for(int n = 0; n < n_neighbors; n++) {
        int cached_i = d2_to_d1(i, n, n_neighbors);
        int neighbor_ii = cached_i;

        int neighbor_i = neighbors[neighbor_ii];
        if(neighbor_i == -1) {
            break;
        }

        h_dip += h_dip_cache[cached_i] * spin[i] * spin[neighbor_i];
    }

    return alpha * h_dip;
}

__kernel void total_fields(
    __global char * spin,
    __global double2 * h_dip_cache,
    double alpha,
    __global double2 * res,
    __global int * neighbors,
    int n_neighbors,
    __global double2 * m,
    __global double2 * h_ext)
{
    int i = get_global_id(0);

    res[i] = h_dip_local(i, spin, h_dip_cache, alpha, neighbors, n_neighbors) +\
             external_field(i, spin, m, h_ext);
}

__kernel void dipolar_fields(
    __global char * spin,
    __global double2 * h_dip_cache,
    double alpha,
    __global double2 * res,
    __global int * neighbors,
    int n_neighbors)
{
    int i = get_global_id(0);
    res[i] = h_dip_local(i, spin, h_dip_cache, alpha, neighbors, n_neighbors);
}

__kernel void external_fields(
    __global char * spin,
    __global double2 * m,
    __global double2 * h_ext,
    __global double2 * res)
{
    int i = get_global_id(0);
    res[i] = external_field(i, spin, m, h_ext);
}

//Calculate the dipolar interaction from this spin(i,j)
//with all of it's neighbors.
__kernel void spin_dipolar_field(
    __global double2 * pos,
    __global double2 * h_dip,
    __global int * neighbors,
    int n_neighbors,
    __global double2 * m)
{
    int i = get_global_id(0);   //spin index
    int q = get_global_id(1);   //neighbor index

    //one thread for each neighbor.
    int ii = d2_to_d1(i, q, n_neighbors);

    //translate neigbor number q to a real neighbor index
    int neighbor_i = neighbors[ii];

    //end of neighbor list marked by -1
    if (neighbor_i == -1) {
        h_dip[ii] = (double2)(0, 0);
        return;
    }

    double2 pos_i = pos[i];
    double2 pos_n = pos[neighbor_i];
    double2 r = pos_n - pos_i;
    double dist = length(r);
    double2 mi = m[i];
    double2 mi_perp = {-mi.y, mi.x};
    double2 mj = m[neighbor_i];

    double2 h_dip_1 = (-1. * mj) / pow(dist, 3);
    double2 h_dip_2 = (3 * r * dot(mj, r)) / pow(dist, 5);
    double2 h_dip_i = h_dip_1 + h_dip_2;

    double h_par = dot(h_dip_i, mi);
    double h_perp = dot(h_dip_i, mi_perp);
    h_dip[ii] = (double2)(h_par, h_perp);
}
