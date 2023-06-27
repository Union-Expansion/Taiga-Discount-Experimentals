import shutil
import os
import sys
import json
import os.path
import urllib.request as req
import paeiou

with open("pa_location.txt") as infile:
    pa_path = os.path.join(infile.readline(), "media/")

gen = "gen"
dl_path = "download"
stage_path = "stage"

mod_urls = {
    "legion": "https://github.com/Legion-Expansion/com.pa.legion-expansion-server/archive/main.zip"
}

def gen_unit_shadows():
    def adj_build_types(units, adjustment):
        for unit_filename in units:
            with open(os.path.join(stage_path, unit_filename[1:])) as unit_file:
                unit = json.load(unit_file)
            unit["buildable_types"] = f"({unit['buildable_types']}){adjustment}"

            out_filename = os.path.join(gen, unit_filename[1:])
            os.makedirs(os.path.dirname(out_filename), exist_ok = True)
            with open(out_filename, "w") as out:
                json.dump(unit, out)

    def override_build_types(unit_filename, new_build):
        with open(os.path.join(stage_path, unit_filename[1:])) as unit_file:
            unit = json.load(unit_file)
        unit["buildable_types"] = new_build

        out_filename = os.path.join(gen, unit_filename[1:])
        os.makedirs(os.path.dirname(out_filename), exist_ok = True)
        with open(out_filename, "w") as out:
            json.dump(unit, out)

    paeiou.simulate_mod_mount(pa_path, mod_urls, dl_path, stage_path)


    # T2 Fabricators can build Experimental Gantry regardless of faction
    adv_fabs = [
        "/pa/units/land/fabrication_bot_adv/fabrication_bot_adv.json",
        "/pa/units/land/bot_support_commander/bot_support_commander.json",
        "/pa/units/land/fabrication_vehicle_adv/fabrication_vehicle_adv.json",
        "/pa/units/air/fabrication_aircraft_adv/fabrication_aircraft_adv.json",
        "/pa/units/air/l_fabrication_aircraft_adv/l_fabrication_aircraft_adv.json",
        "/pa/units/land/l_fabrication_bot_adv/l_fabrication_bot_adv.json",
        "/pa/units/land/l_fabrication_vehicle_adv/l_fabrication_vehicle_adv.json",
        "/pa/units/land/l_bot_support_commander/l_bot_support_commander.json",
    ]
    adj_build_types(adv_fabs, " | (Factory & Titan)")

    # T2 Naval Fabs can build Naval Titan
    adv_naval_fabs = [
        "/pa/units/sea/fabrication_ship_adv/fabrication_ship_adv.json",
        "/pa/units/sea/l_fabrication_ship_adv/l_fabrication_ship_adv.json",
        "/pa/units/orbital/orbital_fabrication_bot/orbital_fabrication_bot.json"
    ]
    adj_build_types(adv_naval_fabs, " | (Naval & Titan)")

    # Legion Orbital Fab can build Naval Titan
    override_build_types("/pa/units/orbital/l_orbital_fabrication_bot/l_orbital_fabrication_bot.json",
        "Custom1 & FabOrbBuild | (Titan - Structure) & Custom1 | Naval & Titan")


def main():
    if os.path.isdir(gen):
        shutil.rmtree(gen)

    shutil.copytree("export", gen, dirs_exist_ok=True)

    paeiou.paeiou( 
        mod_id = "com.pa.daedalus.experimentals", 
        paeiou_unit_path = "PAEIOU_units/", 
        unit_add_list = "unit_add_list.txt", 
        output_path = f"{gen}/",
        mod_prefix = "s17",
        server = True,
        client = False,
        pa_path = pa_path
    )
    gen_unit_shadows()

if __name__ == '__main__':
    main()
