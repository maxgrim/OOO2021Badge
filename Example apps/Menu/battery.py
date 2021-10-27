

def get_battery_percentage(sprite, batteryvalue, chargingstate):
    if chargingstate == True:
        sprite[0] = 0 % 6
        return
    battery_mean_calc = 0
    for x in range(0, 200):
        battery_mean_calc = batteryvalue + battery_mean_calc
        if x == 199:
            battery_mean_calc = int((((battery_mean_calc/200)-34000) * 100)/(41000-34000))
            if battery_mean_calc > 90 and battery_mean_calc < 101:
                sprite[0] = 1 % 6
            if battery_mean_calc > 66 and battery_mean_calc < 90:
                sprite[0] = 2 % 6
            if battery_mean_calc > 33 and battery_mean_calc < 67:
                sprite[0] = 3 % 6
            if battery_mean_calc > 0 and battery_mean_calc < 34:
                sprite[0] = 4 % 6
        x = x + 1

