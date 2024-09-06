import os


# 导入各个模块
from .modules import Make_POTCAR_And_KPOINTS_GW
from .modules import Delete_Files_Except_Ordered_Name
from .modules import Public_Utils

def print_menu():
    os.system('cls' if os.name == 'nt' else 'clear')  # 清屏命令
    print("==================== Huang Tianchang's Tool ====================")
    print("This tool is made for self use, if any problems please email me:")
    print("tianchang.huang@monash.edu. If I have graduated please contact ")
    print("Prof. Nikhil Medhekar (nikhil.medhekar@monash.edu) or Prof. Laure")
    print("Bourgeois (laure.bourgeois@monash.edu) for my new contact details")
    print("")
    print("")
    print("=================== General File Management =====================")
    print(" 101) VASP Input-Files Generator    102) Delete Files          ")
    print(" 103) Copy Files                    104) ")
    print(" 0)  Quit")
    print(" ----------------------------------------------------------------")

def main():
    terminal_directory = Public_Utils.get_terminal_directory()
    program_directory = Public_Utils.get_program_directory()

    while True:
        print_menu()  # 打印菜单
        choice = input("Please select an option (0 to quit): ")

        if choice == '0':
            print("Exiting...")
            break
        elif choice == '101':
            method = int(input("To Use (1) Normal POTCAR (2) GW POTCAR: "))
            Make_POTCAR_And_KPOINTS_GW.run(terminal_directory, program_directory, method) 
        elif choice == '102':
            Delete_Files_Except_Ordered_Name.run(terminal_directory)

"""
        elif choice == '103':
            kpath_band.run()  # 调用kpath_band模块的run()函数
        else:
            print("Invalid option, please try again.")
      
        input("\nPress Enter to continue...")  # 等待用户按下回车键继续
"""
if __name__ == "__main__":
    main()
