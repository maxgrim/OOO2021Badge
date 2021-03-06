EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "OOO 2021 Moon addon"
Date "2021-10-18"
Rev "1"
Comp "Deloitte Risk Advisory B.V."
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 "Authors: Max Grim & James Gratchoff"
$EndDescr
$Comp
L Moon_Addon:ShittyAddon_V1.69bis J1
U 1 1 6158C1FC
P 2400 3600
F 0 "J1" H 2400 3990 50  0000 C CNN
F 1 "ShittyAddon_V1.69bis" H 2400 3899 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical" V 2150 3550 50  0001 C CNN
F 3 "" V 2150 3550 50  0001 C CNN
	1    2400 3600
	1    0    0    -1  
$EndComp
Wire Wire Line
	1900 3450 1850 3450
Wire Wire Line
	1850 3450 1850 3400
$Comp
L power:+3.3V #PWR01
U 1 1 615A54D0
P 1850 3400
F 0 "#PWR01" H 1850 3250 50  0001 C CNN
F 1 "+3.3V" H 1865 3573 50  0000 C CNN
F 2 "" H 1850 3400 50  0001 C CNN
F 3 "" H 1850 3400 50  0001 C CNN
	1    1850 3400
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR02
U 1 1 615A57C1
P 1850 3800
F 0 "#PWR02" H 1850 3550 50  0001 C CNN
F 1 "GND" H 1855 3627 50  0000 C CNN
F 2 "" H 1850 3800 50  0001 C CNN
F 3 "" H 1850 3800 50  0001 C CNN
	1    1850 3800
	1    0    0    -1  
$EndComp
Wire Wire Line
	1850 3800 1850 3750
Wire Wire Line
	1850 3750 1900 3750
NoConn ~ 2900 3450
NoConn ~ 2900 3550
Wire Wire Line
	2900 3650 2950 3650
Text Label 2950 3650 0    50   ~ 0
GPIO1
$Comp
L Device:LED D6
U 1 1 616455D1
P 5925 3250
F 0 "D6" V 5964 3132 50  0000 R CNN
F 1 "LED" V 5873 3132 50  0000 R CNN
F 2 "LED_SMD:LED_0805_2012Metric_Castellated" H 5925 3250 50  0001 C CNN
F 3 "https://lcsc.com/product-detail/Light-Emitting-Diodes-LED_white-0805_C34499.html" H 5925 3250 50  0001 C CNN
F 4 "C34499" V 5925 3250 50  0001 C CNN "LCSC"
	1    5925 3250
	0    -1   -1   0   
$EndComp
$Comp
L Device:R_Small R12
U 1 1 616455D8
P 6225 4300
F 0 "R12" H 6284 4346 50  0000 L CNN
F 1 "10K" H 6284 4255 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.20x1.40mm_HandSolder" H 6225 4300 50  0001 C CNN
F 3 "https://datasheet.lcsc.com/lcsc/1810271610_UNI-ROYAL-Uniroyal-Elec-0805W8F1002T5E_C17414.pdf" H 6225 4300 50  0001 C CNN
F 4 "C17414" H 6225 4300 50  0001 C CNN "LCSC"
	1    6225 4300
	1    0    0    -1  
$EndComp
Wire Wire Line
	6225 4400 6225 4450
$Comp
L power:GND #PWR011
U 1 1 616455DF
P 6225 4450
F 0 "#PWR011" H 6225 4200 50  0001 C CNN
F 1 "GND" H 6230 4277 50  0000 C CNN
F 2 "" H 6225 4450 50  0001 C CNN
F 3 "" H 6225 4450 50  0001 C CNN
	1    6225 4450
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR014
U 1 1 616455E5
P 6575 4550
F 0 "#PWR014" H 6575 4300 50  0001 C CNN
F 1 "GND" H 6580 4377 50  0000 C CNN
F 2 "" H 6575 4550 50  0001 C CNN
F 3 "" H 6575 4550 50  0001 C CNN
	1    6575 4550
	1    0    0    -1  
$EndComp
Wire Wire Line
	6575 4550 6575 4350
Wire Wire Line
	6575 3900 6575 3950
Wire Wire Line
	5925 3100 5925 3050
$Comp
L power:+3.3V #PWR010
U 1 1 616455EE
P 5925 3050
F 0 "#PWR010" H 5925 2900 50  0001 C CNN
F 1 "+3.3V" H 5940 3223 50  0000 C CNN
F 2 "" H 5925 3050 50  0001 C CNN
F 3 "" H 5925 3050 50  0001 C CNN
	1    5925 3050
	1    0    0    -1  
$EndComp
Wire Wire Line
	6275 4150 6225 4150
Wire Wire Line
	6225 4150 6225 4200
$Comp
L Device:R_Small R6
U 1 1 616455F7
P 5925 3550
F 0 "R6" H 5984 3596 50  0000 L CNN
F 1 "15" H 5984 3505 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.20x1.40mm_HandSolder" H 5925 3550 50  0001 C CNN
F 3 "https://datasheet.lcsc.com/lcsc/1810301815_UNI-ROYAL-Uniroyal-Elec-0805W8F150JT5E_C17480.pdf" H 5925 3550 50  0001 C CNN
F 4 "C17480" H 5925 3550 50  0001 C CNN "LCSC"
	1    5925 3550
	1    0    0    -1  
$EndComp
Wire Wire Line
	5925 3400 5925 3450
$Comp
L Device:LED D7
U 1 1 616455FF
P 6250 3250
F 0 "D7" V 6289 3132 50  0000 R CNN
F 1 "LED" V 6198 3132 50  0000 R CNN
F 2 "LED_SMD:LED_0805_2012Metric_Castellated" H 6250 3250 50  0001 C CNN
F 3 "https://lcsc.com/product-detail/Light-Emitting-Diodes-LED_white-0805_C34499.html" H 6250 3250 50  0001 C CNN
F 4 "C34499" V 6250 3250 50  0001 C CNN "LCSC"
	1    6250 3250
	0    -1   -1   0   
$EndComp
Wire Wire Line
	6250 3100 6250 3050
$Comp
L power:+3.3V #PWR012
U 1 1 61645606
P 6250 3050
F 0 "#PWR012" H 6250 2900 50  0001 C CNN
F 1 "+3.3V" H 6265 3223 50  0000 C CNN
F 2 "" H 6250 3050 50  0001 C CNN
F 3 "" H 6250 3050 50  0001 C CNN
	1    6250 3050
	1    0    0    -1  
$EndComp
$Comp
L Device:R_Small R7
U 1 1 6164560D
P 6250 3550
F 0 "R7" H 6309 3596 50  0000 L CNN
F 1 "15" H 6309 3505 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.20x1.40mm_HandSolder" H 6250 3550 50  0001 C CNN
F 3 "https://datasheet.lcsc.com/lcsc/1810301815_UNI-ROYAL-Uniroyal-Elec-0805W8F150JT5E_C17480.pdf" H 6250 3550 50  0001 C CNN
F 4 "C17480" H 6250 3550 50  0001 C CNN "LCSC"
	1    6250 3550
	1    0    0    -1  
$EndComp
Wire Wire Line
	6250 3400 6250 3450
$Comp
L Device:LED D8
U 1 1 61645615
P 6575 3250
F 0 "D8" V 6614 3132 50  0000 R CNN
F 1 "LED" V 6523 3132 50  0000 R CNN
F 2 "LED_SMD:LED_0805_2012Metric_Castellated" H 6575 3250 50  0001 C CNN
F 3 "https://lcsc.com/product-detail/Light-Emitting-Diodes-LED_white-0805_C34499.html" H 6575 3250 50  0001 C CNN
F 4 "C34499" V 6575 3250 50  0001 C CNN "LCSC"
	1    6575 3250
	0    -1   -1   0   
$EndComp
Wire Wire Line
	6575 3100 6575 3050
$Comp
L power:+3.3V #PWR013
U 1 1 6164561C
P 6575 3050
F 0 "#PWR013" H 6575 2900 50  0001 C CNN
F 1 "+3.3V" H 6590 3223 50  0000 C CNN
F 2 "" H 6575 3050 50  0001 C CNN
F 3 "" H 6575 3050 50  0001 C CNN
	1    6575 3050
	1    0    0    -1  
$EndComp
$Comp
L Device:R_Small R8
U 1 1 61645623
P 6575 3550
F 0 "R8" H 6634 3596 50  0000 L CNN
F 1 "15" H 6634 3505 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.20x1.40mm_HandSolder" H 6575 3550 50  0001 C CNN
F 3 "https://datasheet.lcsc.com/lcsc/1810301815_UNI-ROYAL-Uniroyal-Elec-0805W8F150JT5E_C17480.pdf" H 6575 3550 50  0001 C CNN
F 4 "C17480" H 6575 3550 50  0001 C CNN "LCSC"
	1    6575 3550
	1    0    0    -1  
$EndComp
Wire Wire Line
	6575 3400 6575 3450
$Comp
L Device:LED D9
U 1 1 6164562B
P 6925 3250
F 0 "D9" V 6964 3132 50  0000 R CNN
F 1 "LED" V 6873 3132 50  0000 R CNN
F 2 "LED_SMD:LED_0805_2012Metric_Castellated" H 6925 3250 50  0001 C CNN
F 3 "https://lcsc.com/product-detail/Light-Emitting-Diodes-LED_white-0805_C34499.html" H 6925 3250 50  0001 C CNN
F 4 "C34499" V 6925 3250 50  0001 C CNN "LCSC"
	1    6925 3250
	0    -1   -1   0   
$EndComp
Wire Wire Line
	6925 3100 6925 3050
$Comp
L power:+3.3V #PWR015
U 1 1 61645632
P 6925 3050
F 0 "#PWR015" H 6925 2900 50  0001 C CNN
F 1 "+3.3V" H 6940 3223 50  0000 C CNN
F 2 "" H 6925 3050 50  0001 C CNN
F 3 "" H 6925 3050 50  0001 C CNN
	1    6925 3050
	1    0    0    -1  
$EndComp
$Comp
L Device:R_Small R9
U 1 1 61645639
P 6925 3550
F 0 "R9" H 6984 3596 50  0000 L CNN
F 1 "15" H 6984 3505 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.20x1.40mm_HandSolder" H 6925 3550 50  0001 C CNN
F 3 "https://datasheet.lcsc.com/lcsc/1810301815_UNI-ROYAL-Uniroyal-Elec-0805W8F150JT5E_C17480.pdf" H 6925 3550 50  0001 C CNN
F 4 "C17480" H 6925 3550 50  0001 C CNN "LCSC"
	1    6925 3550
	1    0    0    -1  
$EndComp
Wire Wire Line
	6925 3400 6925 3450
$Comp
L Device:LED D10
U 1 1 61645641
P 7275 3250
F 0 "D10" V 7314 3132 50  0000 R CNN
F 1 "LED" V 7223 3132 50  0000 R CNN
F 2 "LED_SMD:LED_0805_2012Metric_Castellated" H 7275 3250 50  0001 C CNN
F 3 "https://lcsc.com/product-detail/Light-Emitting-Diodes-LED_white-0805_C34499.html" H 7275 3250 50  0001 C CNN
F 4 "C34499" V 7275 3250 50  0001 C CNN "LCSC"
	1    7275 3250
	0    -1   -1   0   
$EndComp
Wire Wire Line
	7275 3100 7275 3050
$Comp
L power:+3.3V #PWR016
U 1 1 61645648
P 7275 3050
F 0 "#PWR016" H 7275 2900 50  0001 C CNN
F 1 "+3.3V" H 7290 3223 50  0000 C CNN
F 2 "" H 7275 3050 50  0001 C CNN
F 3 "" H 7275 3050 50  0001 C CNN
	1    7275 3050
	1    0    0    -1  
$EndComp
$Comp
L Device:R_Small R10
U 1 1 6164564F
P 7275 3550
F 0 "R10" H 7334 3596 50  0000 L CNN
F 1 "15" H 7334 3505 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.20x1.40mm_HandSolder" H 7275 3550 50  0001 C CNN
F 3 "https://datasheet.lcsc.com/lcsc/1810301815_UNI-ROYAL-Uniroyal-Elec-0805W8F150JT5E_C17480.pdf" H 7275 3550 50  0001 C CNN
F 4 "C17480" H 7275 3550 50  0001 C CNN "LCSC"
	1    7275 3550
	1    0    0    -1  
$EndComp
Wire Wire Line
	7275 3400 7275 3450
Wire Wire Line
	5925 3900 6250 3900
Wire Wire Line
	5925 3650 5925 3900
Wire Wire Line
	6250 3650 6250 3900
Connection ~ 6250 3900
Wire Wire Line
	6250 3900 6575 3900
Wire Wire Line
	6575 3650 6575 3900
Connection ~ 6575 3900
Wire Wire Line
	6925 3900 6575 3900
Wire Wire Line
	6925 3650 6925 3900
Wire Wire Line
	7275 3650 7275 3900
Connection ~ 6925 3900
$Comp
L Transistor_FET:AO3400A Q2
U 1 1 61645663
P 6475 4150
F 0 "Q2" H 6680 4196 50  0000 L CNN
F 1 "AO3400A" H 6680 4105 50  0000 L CNN
F 2 "Package_TO_SOT_SMD:SOT-23" H 6675 4075 50  0001 L CIN
F 3 "https://datasheet.lcsc.com/lcsc/1811081213_Alpha-&-Omega-Semicon-AO3400A_C20917.pdf" H 6475 4150 50  0001 L CNN
F 4 "C20917" H 6475 4150 50  0001 C CNN "LCSC"
	1    6475 4150
	1    0    0    -1  
$EndComp
Text Label 6175 4150 2    50   ~ 0
GPIO1
Wire Wire Line
	6175 4150 6225 4150
Connection ~ 6225 4150
NoConn ~ 2900 3750
Wire Wire Line
	7275 3900 6925 3900
$EndSCHEMATC
