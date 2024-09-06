import numpy as np
import os
import sys

def parse_poscar(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    lattice_vectors = np.array([list(map(float, line.split())) for line in lines[2:5]])
    return lattice_vectors

def reciprocal_lattice(lattice_vectors):
    volume = np.dot(lattice_vectors[0], np.cross(lattice_vectors[1], lattice_vectors[2]))
    recip_lattice = 2 * np.pi * np.array([
        np.cross(lattice_vectors[1], lattice_vectors[2]) / volume,
        np.cross(lattice_vectors[2], lattice_vectors[0]) / volume,
        np.cross(lattice_vectors[0], lattice_vectors[1]) / volume
    ])
    return recip_lattice

def write_KPOINTS(directory, kspace, lattice_vectors, KPOINTS_filename):
    b = reciprocal_lattice(lattice_vectors)

    if kspace == 0:  # Gamma only
        N = [1, 1, 1]
    else:
        N = np.maximum(np.array([1, 1, 1]), np.round(np.linalg.norm(b, axis=1) / (kspace * 2 * np.pi))).astype(int)

    with open(os.path.join(directory, KPOINTS_filename), 'w') as file:
        file.write("Automatic mesh\n")
        file.write("0\n")
        file.write("Gamma\n")
        file.write(f"{N[0]} {N[1]} {N[2]}\n")
        file.write("0 0 0\n")

def read_element(filepath):
    try:
        with open(filepath, "r") as f:
            line = f.readlines()[5]
        return line.strip().split()
    except FileNotFoundError:
        return []
    
def resource_path(relative_path):
    # 获取资源的绝对路径。用于获取打包的POTCAR文件
    try:
        from importlib.resources import files
        base_path = files('rcs.potpaw_PBE_52')  # 包路径
        return str(base_path.joinpath(relative_path))
    except ImportError:
        # 对于老版本Python或非打包模式下使用
        return os.path.join(os.path.dirname(__file__), 'rcs', 'potpaw_PBE_52', relative_path)


def move_POTCAR_to_dir(program_directory, filepath_destination, element_list, method):
    if method == 1:
        potcar_files = {
            "H": os.path.join(program_directory, "rcs", "potpaw_PBE_52","H", "POTCAR"),
            "He":os.path.join(program_directory, "rcs", "potpaw_PBE_52","He", "POTCAR"),
            "Li":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Li_sv", "POTCAR"),
            "Be":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Be", "POTCAR"),
            "B":os.path.join(program_directory, "rcs", "potpaw_PBE_52","B", "POTCAR"),
            "C":os.path.join(program_directory, "rcs", "potpaw_PBE_52","C", "POTCAR"),
            "N":os.path.join(program_directory, "rcs", "potpaw_PBE_52","N", "POTCAR"),
            "O":os.path.join(program_directory, "rcs", "potpaw_PBE_52","O", "POTCAR"),
            "F":os.path.join(program_directory, "rcs", "potpaw_PBE_52","F", "POTCAR"),
            "Ne":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ne", "POTCAR"),
            "Na":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Na_pv", "POTCAR"),
            "Mg":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Mg", "POTCAR"),
            "Al":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Al", "POTCAR"),
            "Si":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Si", "POTCAR"),
            "P":os.path.join(program_directory, "rcs", "potpaw_PBE_52","P", "POTCAR"),
            "S":os.path.join(program_directory, "rcs", "potpaw_PBE_52","S", "POTCAR"),
            "Cl":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Cl", "POTCAR"),
            "Ar":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ar", "POTCAR"),
            "K":os.path.join(program_directory, "rcs", "potpaw_PBE_52","K_sv", "POTCAR"),
            "Ca":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ca_sv", "POTCAR"),
            "Sc":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Sc_sv", "POTCAR"),
            "Ti":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ti_sv", "POTCAR"),
            "V":os.path.join(program_directory, "rcs", "potpaw_PBE_52","V_sv", "POTCAR"),
            "Cr":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Cr_pv", "POTCAR"),
            "Mn":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Mn_pv", "POTCAR"),
            "Fe":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Fe", "POTCAR"),
            "Co":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Co", "POTCAR"),
            "Ni":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ni", "POTCAR"),
            "Cu":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Cu", "POTCAR"),
            "Zn":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Zn", "POTCAR"),
            "Ga":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ga_d", "POTCAR"),
            "Ge":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ge_d", "POTCAR"),
            "As":os.path.join(program_directory, "rcs", "potpaw_PBE_52","As", "POTCAR"),
            "Se":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Se", "POTCAR"),
            "Br":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Br", "POTCAR"),
            "Kr":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Kr", "POTCAR"),
            "Rb":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Rb_sv", "POTCAR"),
            "Sr":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Sr_sv", "POTCAR"),
            "Y":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Y_sv", "POTCAR"),
            "Zr":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Zr_sv", "POTCAR"),
            "Nb":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Nb_sv", "POTCAR"),
            "Mo":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Mo_sv", "POTCAR"),
            "Tc":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Tc_pv", "POTCAR"),
            "Ru":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ru_pv", "POTCAR"),
            "Rh":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Rh_pv", "POTCAR"),
            "Pd":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Pd", "POTCAR"),
            "Ag":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ag", "POTCAR"),
            "Cd":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Cd", "POTCAR"),
            "In":os.path.join(program_directory, "rcs", "potpaw_PBE_52","In_d", "POTCAR"),
            "Sn":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Sn_d", "POTCAR"),
            "Sb":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Sb", "POTCAR"),
            "Te":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Te", "POTCAR"),
            "I":os.path.join(program_directory, "rcs", "potpaw_PBE_52","I", "POTCAR"),
            "Xe":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Xe", "POTCAR"),
            "Cs":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Cs_sv", "POTCAR"),
            "Ba":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ba_sv", "POTCAR"),
            "La":os.path.join(program_directory, "rcs", "potpaw_PBE_52","La", "POTCAR"),
            "Ce":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ce", "POTCAR"),
            "Pr":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Pr_3", "POTCAR"),
            "Nd":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Nd_3", "POTCAR"),
            "Pm":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Pm_3", "POTCAR"),
            "Sm":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Sm_3", "POTCAR"),
            "Eu":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Eu_2", "POTCAR"),
            "Gd":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Gd_3", "POTCAR"),
            "Tb":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Tb_3", "POTCAR"),
            "Dy":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Dy_3", "POTCAR"),
            "Ho":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ho_3", "POTCAR"),
            "Er":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Er_3", "POTCAR"),
            "Tm":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Tm_3", "POTCAR"),
            "Yb":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Yb_2", "POTCAR"),
            "Lu":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Lu_3", "POTCAR"),
            "Hf":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Hf_pv", "POTCAR"),
            "Ta":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ta_pv", "POTCAR"),
            "W":os.path.join(program_directory, "rcs", "potpaw_PBE_52","W_sv", "POTCAR"),
            "Re":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Re", "POTCAR"),
            "Os":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Os", "POTCAR"),
            "Ir":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ir", "POTCAR"),
            "Pt":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Pt", "POTCAR"),
            "Au":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Au", "POTCAR"),
            "Hg":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Hg", "POTCAR"),
            "Tl":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Tl_d", "POTCAR"),
            "Pb":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Pb_d", "POTCAR"),
            "Bi":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Bi_d", "POTCAR"),
            "Po":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Po_d", "POTCAR"),
            "At":os.path.join(program_directory, "rcs", "potpaw_PBE_52","At", "POTCAR"),
            "Rn":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Rn", "POTCAR"),
            "Fr":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Fr_sv", "POTCAR"),
            "Ra":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ra_sv", "POTCAR"),
            "Ac":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ac", "POTCAR"),
            "Th":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Th", "POTCAR"),
            "Pa":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Pa", "POTCAR"),
            "U":os.path.join(program_directory, "rcs", "potpaw_PBE_52","U", "POTCAR"),
            "Np":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Np", "POTCAR"),
            "Pu":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Pu", "POTCAR"),
            "Am":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Am", "POTCAR"),
            "Cm":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Cm", "POTCAR")}
    elif method == 2:
        # 定义一个字典，将元素映射到其对应的 POTCAR 文件路径
        potcar_files = {
        "H": os.path.join(program_directory, "rcs", "potpaw_PBE_52","H_GW", "POTCAR"),
        "He":os.path.join(program_directory, "rcs", "potpaw_PBE_52","He_GW", "POTCAR"),
        "Li":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Li_sv_GW", "POTCAR"),
        "Be":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Be_sv_GW", "POTCAR"),
        "B":os.path.join(program_directory, "rcs", "potpaw_PBE_52","B_GW", "POTCAR"),
        "C":os.path.join(program_directory, "rcs", "potpaw_PBE_52","C_GW", "POTCAR"),
        "N":os.path.join(program_directory, "rcs", "potpaw_PBE_52","N_GW", "POTCAR"),
        "O":os.path.join(program_directory, "rcs", "potpaw_PBE_52","O_GW", "POTCAR"),
        "F":os.path.join(program_directory, "rcs", "potpaw_PBE_52","F_GW", "POTCAR"),
        "Ne":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ne_GW", "POTCAR"),
        "Na":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Na_sv_GW", "POTCAR"),
        "Mg":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Mg_sv_GW", "POTCAR"),
        "Al":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Al_GW", "POTCAR"),
        "Si":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Si_GW", "POTCAR"),
        "P":os.path.join(program_directory, "rcs", "potpaw_PBE_52","P_GW", "POTCAR"),
        "S":os.path.join(program_directory, "rcs", "potpaw_PBE_52","S_GW", "POTCAR"),
        "Cl":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Cl_GW", "POTCAR"),
        "Ar":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ar_GW", "POTCAR"),
        "K":os.path.join(program_directory, "rcs", "potpaw_PBE_52","K_sv_GW", "POTCAR"),
        "Ca":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ca_sv_GW", "POTCAR"),
        "Sc":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Sc_sv_GW", "POTCAR"),
        "Ti":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ti_sv_GW", "POTCAR"),
        "V":os.path.join(program_directory, "rcs", "potpaw_PBE_52","V_sv_GW", "POTCAR"),
        "Cr":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Cr_sv_GW", "POTCAR"),
        "Mn":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Mn_sv_GW", "POTCAR"),
        "Fe":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Fe_sv_GW", "POTCAR"),
        "Co":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Co_sv_GW", "POTCAR"),
        "Ni":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ni_sv_GW", "POTCAR"),
        "Cu":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Cu_sv_GW", "POTCAR"),
        "Zn":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Zn_sv_GW", "POTCAR"),
        "Ga":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ga_d_GW", "POTCAR"),
        "Ge":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ge_d_GW", "POTCAR"),
        "As":os.path.join(program_directory, "rcs", "potpaw_PBE_52","As_GW", "POTCAR"),
        "Se":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Se_GW", "POTCAR"),
        "Br":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Br_GW", "POTCAR"),
        "Kr":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Kr_GW", "POTCAR"),
        "Rb":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Rb_sv_GW", "POTCAR"),
        "Sr":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Sr_sv_GW", "POTCAR"),
        "Y":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Y_sv_GW", "POTCAR"),
        "Zr":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Zr_sv_GW", "POTCAR"),
        "Nb":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Nb_sv_GW", "POTCAR"),
        "Mo":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Mo_sv_GW", "POTCAR"),
        "Tc":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Tc_sv_GW", "POTCAR"),
        "Ru":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ru_sv_GW", "POTCAR"),
        "Rh":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Rh_sv_GW", "POTCAR"),
        "Pd":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Pd_sv_GW", "POTCAR"),
        "Ag":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ag_sv_GW", "POTCAR"),
        "Cd":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Cd_sv_GW", "POTCAR"),
        "In":os.path.join(program_directory, "rcs", "potpaw_PBE_52","In_d_GW", "POTCAR"),
        "Sn":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Sn_d_GW", "POTCAR"),
        "Sb":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Sb_d_GW", "POTCAR"),
        "Te":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Te_GW", "POTCAR"),
        "I":os.path.join(program_directory, "rcs", "potpaw_PBE_52","I_GW", "POTCAR"),
        "Xe":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Xe_GW", "POTCAR"),
        "Cs":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Cs_sv_GW", "POTCAR"),
        "Ba":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ba_sv_GW", "POTCAR"),
        "La":os.path.join(program_directory, "rcs", "potpaw_PBE_52","La_GW", "POTCAR"),
        "Ce":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ce_GW", "POTCAR"),
        "Pr":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Hf_sv_GW", "POTCAR"),
        "Nd":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Nd_3", "POTCAR"),
        "Pm":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Pm_3", "POTCAR"),
        "Sm":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Sm_3", "POTCAR"),
        "Eu":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Eu_2", "POTCAR"),
        "Gd":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Gd_3", "POTCAR"),
        "Tb":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Tb_3", "POTCAR"),
        "Dy":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Dy_3", "POTCAR"),
        "Ho":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ho_3", "POTCAR"),
        "Er":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Er_3", "POTCAR"),
        "Tm":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Tm_3", "POTCAR"),
        "Yb":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Yb_2", "POTCAR"),
        "Lu":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Lu_3", "POTCAR"),
        "Hf":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Hf_pv", "POTCAR"),
        "Ta":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ta_sv_GW", "POTCAR"),
        "W":os.path.join(program_directory, "rcs", "potpaw_PBE_52","W_sv_GW", "POTCAR"),
        "Re":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Re_sv_GW", "POTCAR"),
        "Os":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Os_sv_GW", "POTCAR"),
        "Ir":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ir_sv_GW", "POTCAR"),
        "Pt":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Pt_sv_GW", "POTCAR"),
        "Au":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Au_sv_GW", "POTCAR"),
        "Hg":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Hg_sv_GW", "POTCAR"),
        "Tl":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Tl_d_GW", "POTCAR"),
        "Pb":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Pb_d_GW", "POTCAR"),
        "Bi":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Bi_d_GW", "POTCAR"),
        "Po":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Po_d_GW", "POTCAR"),
        "At":os.path.join(program_directory, "rcs", "potpaw_PBE_52","At_d_GW", "POTCAR"),
        "Rn":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Rn_d_GW", "POTCAR"),
        "Fr":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Fr_sv", "POTCAR"),
        "Ra":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ra_sv", "POTCAR"),
        "Ac":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Ac", "POTCAR"),
        "Th":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Th", "POTCAR"),
        "Pa":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Pa", "POTCAR"),
        "U":os.path.join(program_directory, "rcs", "potpaw_PBE_52","U", "POTCAR"),
        "Np":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Np", "POTCAR"),
        "Pu":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Pu", "POTCAR"),
        "Am":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Am", "POTCAR"),
        "Cm":os.path.join(program_directory, "rcs", "potpaw_PBE_52","Cm", "POTCAR")}

    # 用于存储所有元素的 POTCAR 内容
    elements_POTCAR = {}

    for element in element_list:
        potcar_path = potcar_files.get(element)  # 获取对应的 POTCAR 路径
        if potcar_path:
            with open(potcar_path, 'r') as file:
                elements_POTCAR[element + "_POTCAR"] = file.read()

    # 将所有读取的 POTCAR 内容写入目标文件
    with open(filepath_destination, 'w') as file:
        for key in elements_POTCAR:
            file.write(elements_POTCAR[key])

    return None



def process_directory(terminal_directory, program_directory, kspace, method, KPOINTS_filename):
    poscar_path = os.path.join(terminal_directory, "POSCAR")
    if os.path.exists(poscar_path):
        lattice_vectors = parse_poscar(poscar_path)
        write_KPOINTS(terminal_directory, kspace, lattice_vectors, KPOINTS_filename)
        
        elements = read_element(poscar_path)
        if elements:
            potcar_destination = os.path.join(terminal_directory, "POTCAR")  # 正确的目标文件路径
            move_POTCAR_to_dir(program_directory, potcar_destination, elements, method)


def run(terminal_directory, program_directory, method):

    incar1 = """
SYSTEM = Default

# Starting parameters for this run:
   ISTART =      0     job   : 0-new, 1-cont, 2-samecut
   ICHARG =      2     charge: 0-wave, 1-file, 2-atom, >10-const
   INIWAV =      1     electr: 0-lowe 1-rand  2-diag

# Electronic Relaxation:
   PREC    = normal      "precision"-mode.
   ADDGRID = .TRUE.     reduce the noise in the forces
   SYMPREC = 1E-5      Default is 1E-5
   ENCUT   = 500.0      Default is set by emax and emin
#  NGX     = 26             

#  NELMDL = -7        number of delayed ELM steps
#  NELM   = 101       number of ELM steps
   EDIFF  = 1E-5     energy stopping-criterion for ELM, Default EDIFF = 1E-04
   LREAL  = Auto   real-space projection (.FALSE.--for very small cells/accurate charge density, .TRUE., On, Auto)
   ALGO   = fast    algorithm for electronic minimisation (normal: DAV, veryfast: RMM, fast: DAV+RMM)
#  WEIMIN = 0         stabilises RMM algo 

# Writing files:
   LCHARG  = .FALSE.    write electronic charge density
   LWAVE   = .FALSE.   writes WAVECAR
#  LVTOT   = .FALSE.   
#   LORBIT =     11     writes DOSCAR

# Ionic Relaxation:
   NSW    =    500     max number of geometry steps
   IBRION =     2     ionic relax: 0-MD, 1-quasi-Newton, 2-CG, 3-Damped MD
   EDIFFG =    1E-4  force (eV/A) stopping-criterion for geometry steps
   ISIF   =     3     (force|stress|ions|shape|vol 0:ynynn 1:yyynn 2:yyynn 3:yyyyy)
   ISYM   =     1     (1-use symmetry, 0-no symmetry)

# DOS related values:
#   NEDOS  =     3201   Default is 301
   ISMEAR =     1      (-1-Fermi, 1-Methfessel/Paxton, 0:Gaussian, -5:Blochl tetrahedron)
   SIGMA  =     0.1    broadening in eV

# Spin-polarized calculations:
   ISPIN = 1           (1-non-spin, 2-spin)
#  MAGMOM = 71*0 1   

# +U or not +U
#   LDAU = .TRUE.
#   LDAUTYPE = 	2
#   LDAUL = 		(-1-No+U, 1-p orbit, 2-d orbit, 3-f orbit)
#   LDAUU = 		(specify U)
#   LDAUJ = 		(specify J)
#   LMAXMIX =		(2/4/6)

#Dipole moment
# IDIPOL = 3        
# LDIPOL = .TRUE.   
# LORBIT = 11

#Van Der Waals interaction
#   IVDW = 11   Uses DFT-D3 from Grimme's paper to add corrections van der waals

# Parallelization flags:
#   NPAR   =  16   ( =1: all nodes work on each band, = else: only one node will work on each band)
   LPLANE = .TRUE. (parallelization of plane wave coefficients)
   NCORE = 16
    """

    incar2 = """
SYSTEM = Default

# Starting parameters for this run:
   ISTART =      0     job   : 0-new, 1-cont, 2-samecut
   ICHARG =      2     charge: 0-wave, 1-file, 2-atom, >10-const
   INIWAV =      1     electr: 0-lowe 1-rand  2-diag

# Electronic Relaxation:
   PREC    = accurate      "precision"-mode.
   ADDGRID = .TRUE.     reduce the noise in the forces
   SYMPREC = 1E-5      Default is 1E-5
   ENCUT   = 600.0      Default is set by emax and emin
#  NGX     = 26             

#  NELMDL = -7        number of delayed ELM steps
#  NELM   = 101       number of ELM steps
   EDIFF  = 1E-5     energy stopping-criterion for ELM, Default EDIFF = 1E-04
   LREAL  = .FALSE.   real-space projection (.FALSE.--for very small cells/accurate charge density, .TRUE., On, Auto)
   ALGO   = normal    algorithm for electronic minimisation (normal: DAV, veryfast: RMM, fast: DAV+RMM)
#  WEIMIN = 0         stabilises RMM algo 

# Writing files:
   LCHARG  = .FALSE.    write electronic charge density
   LWAVE   = .FALSE.   writes WAVECAR
#  LVTOT   = .FALSE.   
#   LORBIT =     11     writes DOSCAR

# Ionic Relaxation:
   NSW    =    0     max number of geometry steps
   IBRION =     2     ionic relax: 0-MD, 1-quasi-Newton, 2-CG, 3-Damped MD
   EDIFFG =    1E-4  force (eV/A) stopping-criterion for geometry steps
   ISIF   =     3     (force|stress|ions|shape|vol 0:ynynn 1:yyynn 2:yyynn 3:yyyyy)
   ISYM   =     1     (1-use symmetry, 0-no symmetry)

# DOS related values:
#   NEDOS  =     3201   Default is 301
   ISMEAR =     1      (-1-Fermi, 1-Methfessel/Paxton, 0:Gaussian, -5:Blochl tetrahedron)
   SIGMA  =     0.05    broadening in eV

# Spin-polarized calculations:
   ISPIN = 2           (1-non-spin, 2-spin)
#  MAGMOM = 71*0 1   

# +U or not +U
#   LDAU = .TRUE.
#   LDAUTYPE = 	2
#   LDAUL = 		(-1-No+U, 1-p orbit, 2-d orbit, 3-f orbit)
#   LDAUU = 		(specify U)
#   LDAUJ = 		(specify J)
#   LMAXMIX =		(2/4/6)

#Dipole moment
# IDIPOL = 3        
# LDIPOL = .TRUE.   
# LORBIT = 11

#Van Der Waals interaction
#   IVDW = 11   Uses DFT-D3 from Grimme's paper to add corrections van der waals

# Parallelization flags:
#   NPAR   =  16   ( =1: all nodes work on each band, = else: only one node will work on each band)
   LPLANE = .TRUE. (parallelization of plane wave coefficients)
   NCORE = 16
    """

    jobfile = """
#!/bin/bash -l
#SBATCH --account=pawsey0416
#SBATCH --partition=work
#SBATCH --ntasks=256
#SBATCH --nodes=2
#SBATCH --exclusive
#SBATCH --time=24:00:00


module load vasp/5.4.4

cp KPOINTS.1 KPOINTS
cp INCAR.1 INCAR
cp POSCAR POSCAR.1

srun -n 256 -N 2 vasp_std

cp CONTCAR POSCAR
cp CONTCAR POSCAR.2
cp XDATCAR XDATCAR.1
cp OUTCAR OUTCAR.1

cp KPOINTS.2 KPOINTS
cp INCAR.2 INCAR

srun -n 256 -N 2 vasp_std
    """
    
    for subdir, dirs, files in os.walk(terminal_directory):
        process_directory(subdir, program_directory, 0.02, method, "KPOINTS.1")
        process_directory(subdir, program_directory, 0.015, method, "KPOINTS.2")

        # 创建并写入INCAR.1文件
        with open(os.path.join(subdir, 'INCAR.1'), 'w') as f:
            f.write(incar1)
        
        # 创建并写入INCAR.2文件
        with open(os.path.join(subdir, 'INCAR.2'), 'w') as f:
            f.write(incar2)

        # 创建并写入job文件
        with open(os.path.join(subdir, 'job.sh'), 'w') as f:
            f.write(jobfile)
    input ("File Writing Successful! Press Any Key To Continue...")