
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
    