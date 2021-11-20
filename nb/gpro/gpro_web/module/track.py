import os
from django import apps

def trackdata_dict_create():
    with open(f"{os.path.join(os.path.dirname(__file__), 'Track.csv')}") as track:
        count = 0
        for line in track:
            linedict = dict()
            lines = line.split(";")
            lines[-1] = lines[-1].replace('\n','')
            if not lines[-1]:
                lines[-1] = "0.0%"
            if not lines[18]:
                lines[18] = 0.0
            if count != 0:
                linedict = {'ktrack': lines[1], 
                            'laps': int(lines[2]),
                            'pit': float(lines[3]),
                            'con': int(lines[4]),
                            'agg': int(lines[5]),
                            'exp': int(lines[6]),
                            'ti': int(lines[7]),
                            'eng': int(lines[8]),
                            'ele': int(lines[9]),
                            'hum': float(lines[10]),
                            'fuel': float(lines[11]),
                            'wings': float(lines[12]),
                            'eng_set': float(lines[13]),
                            'bra': float(lines[14]),
                            'gea': float(lines[15]),
                            'sus': float(lines[16]),
                            'comments': lines[17],
                            'ws': float(lines[18]),
                            'actual': lines[19],
                            'formula': lines[20],
                            'difference': lines[21],
                            'wc': float(lines[22].replace('%','')),
                            'track': lines[23],
                            'power': int(lines[24]),
                            'handling': int(lines[25]),
                            'acceleration': int(lines[26]),
                            'downforce': int(lines[27]),
                            'overtaking': int(lines[28]),
                            'suspension_track': int(lines[29]),
                            'corners': int(lines[30]),
                            'length': float(lines[31]),
                            'tyre_wear': int(lines[32]),
                            'fuel_wear': int(lines[33]),
                            'cha_wear': float(lines[34]),
                            'eng_wear': float(lines[35]),
                            'fw_wear': float(lines[36]),
                            'rw_wear': float(lines[37]),
                            'und_wear': float(lines[38]),
                            'sid_wear': float(lines[39]),
                            'coo_wear': float(lines[40]),
                            'gea_wear': float(lines[41]),
                            'bra_wear': float(lines[42]),
                            'sus_wear': float(lines[43]),
                            'ele_wear': float(lines[44]),
                            'ctrack2': float(lines[45].replace('%',''))/100,
                            'ctrack': float(lines[46].replace('%',''))
                }
                trackdata[str(lines[0])] = linedict
            count += 1

trackdata = dict()
trackdata_dict_create()
"""
track = apps.apps.get_model('gpro', 'Track')
for k in trackdata.keys():
    t = track(name=k)
    t.save()
"""