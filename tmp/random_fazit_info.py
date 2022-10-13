"""
REF:
SVW	SAP PN
FAW-VW	SAP PN	Chassis_DMC	FAN_DMC	PCB_DMC
X9G-10212.10.2299990601	97003-443/8000	09815-01100112001/09/2022	98151N8001DC	00889920990001


SVW	SAP PN
Chassis_DMC	FAN_DMC	PCB_DMC
X9G-10111.10.2299990601	97003-442/8000	09815-01100112001/10/2022	98151N9001CQ	00889920980001

"""
import pprint

"""
98151N8001DC
98151N8001DO
98151N8001DS
"""

def base36_encode(number):
    num_str = '0123456789abcdefghijklmnopqrstuvwxyz'
    if number == 0:
        return '0'

    base36 = []
    while number != 0:
        number, i = divmod(number, 36)    # 返回 number// 36 , number%36
        base36.append(num_str[i])

    return ''.join(reversed(base36))



class Fazit:
    def __init__(self,year,month):
        self.year = year
        self.month = month
        self.chassis = []
        self.fans = []
        self.pcbs = []

    @staticmethod
    def base36_encode(number):
        num_str = '0123456789abcdefghijklmnopqrstuvwxyz'
        if number == 0:
            return '0'

        base36 = []
        while number != 0:
            number, i = divmod(number, 36)  # 返回 number// 36 , number%36
            base36.append(num_str[i])

        return ''.join(reversed(base36))

    def set_RD_chassis_DMC(self,r_start, numbers):
        self.chassis = ["09815-01100112%03d/%s/%s"%(x,self.month,self.year) for x in range(r_start,r_start + numbers)]
        # return ["09815-01100112%03d/%s/%s"%(x,self.month,self.year) for x in range(r_start,r_stop)]

    def set_RD_FAN_DMC(self, r_start, numbers):
        self.fans = [base36_encode(i).upper() for i in range(r_start,r_start + numbers)]

    def set_RD_PCB_DMC(self, r_start, numbers):
        self.pcbs = ["0088992099%04d"%i for i in range(r_start, r_start + numbers)]



if __name__ == '__main__':
    FAW = Fazit("2022","10")
    FAW.set_RD_chassis_DMC(1,200)
    FAW.set_RD_FAN_DMC(1213960396279136862,200)
    FAW.set_RD_PCB_DMC(1,200)
    with open("FAW_fazit_info.txt", "w") as file:
        # file.write("Chassis_DMC\tFAN_DMC\tPCB_DMC\n")
        # file.write("%<26s%s%s\n"%("Chassis_DMC","FAN_DMC","PCB_DMC"))
        file.write("{:<25s}\t{:<12s}\t{:<14s}\n".format("Chassis_DMC", "FAN_DMC", "PCB_DMC"))
        for i,j,k in zip(FAW.chassis,FAW.fans,FAW.pcbs):
            # print(i)
            file.write(f"{i}\t{j}\t{k}\n")


    SVW = Fazit("2022", "10")
    SVW.set_RD_chassis_DMC(201, 200)
    SVW.set_RD_FAN_DMC(1213960396279137062, 200)
    SVW.set_RD_PCB_DMC(201, 200)
    with open("SVW_fazit_info.txt", "w") as file:
        # file.write("Chassis_DMC\tFAN_DMC\tPCB_DMC\n")
        # file.write("%<26s%s%s\n"%("Chassis_DMC","FAN_DMC","PCB_DMC"))
        file.write("{:<25s}\t{:<12s}\t{:<14s}\n".format("Chassis_DMC", "FAN_DMC", "PCB_DMC"))
        for i, j, k in zip(SVW.chassis, SVW.fans, SVW.pcbs):
            # print(i)
            file.write(f"{i}\t{j}\t{k}\n")




    # print(base36_encode(1213960396279136691).upper())
    # FAN_DMC_list = []
    # with open("temp_data.txt","r") as file:
    #     data = file.readlines()
    #     for i in data[1:]:
    #         FAN_DMC_list.append(i.strip())
    #
    #
    # print(FAN_DMC_list)
    # FAN_DMC_list_to_dec = [int(num,36) for num in FAN_DMC_list]
    # FAN_DMC_list_to_dec.sort()
    # pprint.pprint(FAN_DMC_list_to_dec)
    #
    num_36_start = 1213960396279136862


