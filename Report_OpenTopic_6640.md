![A black and white logo Description automatically
generated](media/image1.png){width="1.6527777777777777in"
height="1.3472222222222223in"}

ชื่อโครงงาน Force feedback in RC car scale

นายภารุจ เอื้อสุดกิจ

โครงงานนี้เป็นส่วนหนึ่งของการศึกษาตามหลักสูตร

ปริญญาวิศวกรรมศาสตรบัณฑิต  สาขาวิชาวิศวกรรมหุ่นยนต์และระบบอัตโนมัติ

สถาบันวิทยาการหุ่นยนต์ภาคสนาม

มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี

ปีการศึกษา 2568

# สารบัญ {#สารบญ .TOC-Heading}

[บทที่ 1 บทนำ [4](#บทท-1-บทนำ)](#บทท-1-บทนำ)

[1.1 ที่มา ความสำคัญ [4](#ทมา-ความสำคญ)](#ทมา-ความสำคญ)

[1.2 ประโยคปัญหางานวิจัย (Problem Statement)
[4](#ประโยคปญหางานวจย-problem-statement)](#ประโยคปญหางานวจย-problem-statement)

[1.3 ผลผลิตและผลลัพธ์ (Outputs and Outcomes)
[4](#ผลผลตและผลลพธ-outputs-and-outcomes)](#ผลผลตและผลลพธ-outputs-and-outcomes)

[ผลผลิต [4](#ผลผลต)](#ผลผลต)

[ผลลัพธ์ [4](#ผลลพธ)](#ผลลพธ)

[1.4 ความต้องการของระบบ (Requirements)
[4](#ความตองการของระบบ-requirements)](#ความตองการของระบบ-requirements)

[1.5 ขอบเขตของงานวิจัย (Scopes)
[5](#ขอบเขตของงานวจย-scopes)](#ขอบเขตของงานวจย-scopes)

[1.6 ข้อกำหนดของงานวิจัย (Assumptions)
[5](#ขอกำหนดของงานวจย-assumptions)](#ขอกำหนดของงานวจย-assumptions)

[1.7 ขั้นตอนการดำเนินงาน [5](#ขนตอนการดำเนนงาน)](#ขนตอนการดำเนนงาน)

[บทที่ 2 ทฤษฎี/งานวิจัย/การศึกษาที่เกี่ยวข้อง
[6](#บทท-2-ทฤษฎงานวจยการศกษาทเกยวของ)](#บทท-2-ทฤษฎงานวจยการศกษาทเกยวของ)

[2.1 แนวคิดพวงมาลัยเสมือนสำหรับ Force Feedback (Virtual Wheel Concept)
[6](#แนวคดพวงมาลยเสมอนสำหรบ-force-feedback-virtual-wheel-concept)](#แนวคดพวงมาลยเสมอนสำหรบ-force-feedback-virtual-wheel-concept)

[2.1.1 แรงต้านทานแบบพาสซีฟ (Passive Resistive Forces)
[6](#แรงตานทานแบบพาสซฟ-passive-resistive-forces)](#แรงตานทานแบบพาสซฟ-passive-resistive-forces)

[2.1.2 แรงเชิงรุก (Active Restorative Forces)
[6](#แรงเชงรก-active-restorative-forces)](#แรงเชงรก-active-restorative-forces)

[2.2 สมการพื้นฐานของระบบ Force Feedback
[6](#สมการพนฐานของระบบ-force-feedback)](#สมการพนฐานของระบบ-force-feedback)

[2.3 ระบบ Virtual Vehicle สำหรับ Steer-by-Wire
[7](#ระบบ-virtual-vehicle-สำหรบ-steer-by-wire)](#ระบบ-virtual-vehicle-สำหรบ-steer-by-wire)

[2.4 การประมาณค่าแรงจากยางและการตรวจจับการลื่นไถล
[7](#การประมาณคาแรงจากยางและการตรวจจบการลนไถล)](#การประมาณคาแรงจากยางและการตรวจจบการลนไถล)

[2.5 การออกแบบระบบ Haptic Feedback สำหรับ Steering
[7](#การออกแบบระบบ-haptic-feedback-สำหรบ-steering)](#การออกแบบระบบ-haptic-feedback-สำหรบ-steering)

[2.6 การประเมินระบบ Steering ด้วย Haptic Feedback
[7](#การประเมนระบบ-steering-ดวย-haptic-feedback)](#การประเมนระบบ-steering-ดวย-haptic-feedback)

[บทที่ 3 ระเบียบวิธีวิจัย [8](#บทท-3-ระเบยบวธวจย)](#บทท-3-ระเบยบวธวจย)

[3.1 สถาปัตยกรรมระบบ [8](#สถาปตยกรรมระบบ)](#สถาปตยกรรมระบบ)

[3.2 ฮาร์ดแวร์ [8](#ฮารดแวร)](#ฮารดแวร)

[3.2.1 รายละเอียดเซนเซอร์ที่ใช้
[8](#รายละเอยดเซนเซอรทใช)](#รายละเอยดเซนเซอรทใช)

[3.2.2 รายละเอียดรถบังคับวิทยุที่ใช้
[9](#รายละเอยดรถบงคบวทยทใช)](#รายละเอยดรถบงคบวทยทใช)

[3.2.3 รายละเอียดอุปรณ์บังคับรถที่ใช้
[10](#รายละเอยดอปรณบงคบรถทใช)](#รายละเอยดอปรณบงคบรถทใช)

[3.3 ระบบการสื่อสาร [10](#ระบบการสอสาร)](#ระบบการสอสาร)

[3.4 อัลกอริทึมการคำนวณแรง Force Feedback
[11](#อลกอรทมการคำนวณแรง-force-feedback)](#อลกอรทมการคำนวณแรง-force-feedback)

[3.4.1 สูตรหลัก (จาก Balachandran et al., 2014)
[11](#สตรหลก-จาก-balachandran-et-al.-2014)](#สตรหลก-จาก-balachandran-et-al.-2014)

[3.4.2 แรงต้านทานแบบพาสซีฟ (Passive Resistive)
[11](#แรงตานทานแบบพาสซฟ-passive-resistive)](#แรงตานทานแบบพาสซฟ-passive-resistive)

[3.4.3 แรงเชิงรุก (Active Restorative)
[12](#แรงเชงรก-active-restorative)](#แรงเชงรก-active-restorative)

[3.4.1 การประมาณความเร็ว (Velocity Estimation)
[12](#การประมาณความเรว-velocity-estimation)](#การประมาณความเรว-velocity-estimation)

[3.4.1 การตรวจจับการลื่นไถล (Drift Detection)
[12](#การตรวจจบการลนไถล-drift-detection)](#การตรวจจบการลนไถล-drift-detection)

[บทที่ 4 การทดลองและผลการทดลอง/วิจัย
[13](#บทท-4-การทดลองและผลการทดลองวจย)](#บทท-4-การทดลองและผลการทดลองวจย)

[4.1 วิธีการทดสอบประสิทธิภาพ
[13](#วธการทดสอบประสทธภาพ)](#วธการทดสอบประสทธภาพ)

[4.1.1 Latency Test [13](#latency-test)](#latency-test)

[4.1.2 Range Test [13](#range-test)](#range-test)

[4.1.3 การทดสอบการทำงานของ Current Sensor (ACS712)
[14](#การทดสอบการทำงานของ-current-sensor-acs712)](#การทดสอบการทำงานของ-current-sensor-acs712)

[4.1.4 การทดสอบเพื่อ Calibrate Loadcell (HX711)
[14](#การทดสอบเพอ-calibrate-loadcell-hx711)](#การทดสอบเพอ-calibrate-loadcell-hx711)

[4.1.5 การทดสอบองค์ประกอบ FFB (Component Validation)
[14](#การทดสอบองคประกอบ-ffb-component-validation)](#การทดสอบองคประกอบ-ffb-component-validation)

[4.1.6 การทดสอบเชิงปริมาณ (Quantitative Test)
[16](#การทดสอบเชงปรมาณ-quantitative-test)](#การทดสอบเชงปรมาณ-quantitative-test)

[4.2 ผลการทดลอง [17](#ผลการทดลอง)](#ผลการทดลอง)

[4.2.1 Latency Test Results
[17](#latency-test-results)](#latency-test-results)

[4.2.2 Range Test Results
[18](#range-test-results)](#range-test-results)

[4.2.3 ผลการทดสอบการทำงานของ Current Sensor (ACS712)
[19](#ผลการทดสอบการทำงานของ-current-sensor-acs712)](#ผลการทดสอบการทำงานของ-current-sensor-acs712)

[4.2.4 ผลการทดสอบเพื่อ Calibrate Load Cell (HX711)
[20](#ผลการทดสอบเพอ-calibrate-load-cell-hx711)](#ผลการทดสอบเพอ-calibrate-load-cell-hx711)

[4.2.5 ผลการทดสอบองค์ประกอบ FFB (Component Validation)
[21](#ผลการทดสอบองคประกอบ-ffb-component-validation)](#ผลการทดสอบองคประกอบ-ffb-component-validation)

[4.2.6 ผลการทดสอบเชิงปริมาณ (Quantitative Test)
[28](#ผลการทดสอบเชงปรมาณ-quantitative-test)](#ผลการทดสอบเชงปรมาณ-quantitative-test)

[บทที่ 5 บทสรุป [29](#บทท-5-บทสรป)](#บทท-5-บทสรป)

[5.1 สรุปผลการดำเนินงาน [29](#สรปผลการดำเนนงาน)](#สรปผลการดำเนนงาน)

[5.2 ความสำเร็จที่ได้รับ [29](#ความสำเรจทไดรบ)](#ความสำเรจทไดรบ)

[5.3 ข้อจำกัด [29](#ขอจำกด)](#ขอจำกด)

[5.4 แนวทางการพัฒนาในอนาคต
[30](#แนวทางการพฒนาในอนาคต)](#แนวทางการพฒนาในอนาคต)

[เอกสารอ้างอิง [31](#เอกสารอางอง)](#เอกสารอางอง)

# บทที่ 1 บทนำ

## 1.1 ที่มา ความสำคัญ 

รถบังคับวิทยุ (RC cars) ในปัจจุบันมักใช้ตัวส่งสัญญาณแบบ Pistol-grip
ซึ่งขาดการตอบสนองเชิงฟิสิกส์ (Physical feedback) ไปยังผู้ขับขี่
ผู้ขับขี่จึงได้รับเพียงข้อมูลทางสายตา (Visual feedback)
ทำให้ขาดความสมจริงและไม่สามารถรับรู้พฤติกรรมของรถในขณะนั้นได้

## 1.2 ประโยคปัญหางานวิจัย (Problem Statement)

เนื่องจากตัวส่งสัญญาณแบบเดิมไม่สามารถให้ข้อมูลการขับขี่ที่สมจริง จึงจำเป็นต้องพัฒนา
\"Steering force feedback system" สำหรับรถบังคับวิทยุ
เพื่อสะท้อนพฤติกรรมของยานพาหนะให้ผู้ขับขี่รับรู้และสร้างความรู้สึกการบังคับที่สมจริง

## 1.3 ผลผลิตและผลลัพธ์ (Outputs and Outcomes)

### ผลผลิต

ระบบ Force Feedback System สำหรับรถบังคับวิทยุที่ทำงานผ่านการเชื่อมต่อไร้สาย

### ผลลัพธ์

ผู้ขับขี่สามารถรับรู้พฤติกรรมของรถผ่านแรงตอบสนองบนพวงมาลัย
ทำให้การควบคุมมีความสมจริงมากขึ้น

## 1.4 ความต้องการของระบบ (Requirements)

1.  สร้างแรงต้าน (Resistive torque) ได้แปรผัน

2.  ส่งข้อมูลไร้สายได้ระยะอย่างน้อย 20 เมตร

3.  ความหน่วง (Latency) ต่ำกว่า 70 ms

4.  ความรู้สึกการตอบสนองเป็นธรรมชาติ

## 1.5 ขอบเขตของงานวิจัย (Scopes)

1.  ออกแบบระบบ Force feedback แบบจำลองโดยใช้พวงมาลัย Thrustmaster T248

2.  ใช้เซนเซอร์วัดกระแส (Current sensor) และ Force sensor เพื่อวัดแรงที่กระทำกับ
    Servo และใช้ IMU เพื่อประมวลผลระบบควบคุม

## 1.6 ข้อกำหนดของงานวิจัย (Assumptions)

สมมติว่าตำแหน่งพวงมาลัยจากตัวควบคุมตรงกับตำแหน่งล้อหน้า เนื่องจาก Servo
มีความเร็วและแรงเพียงพอ

## 1.7 ขั้นตอนการดำเนินงาน 

  ------------------------------------------------------------------------------------------------------------
  ระยะ             1   2   3   4   5   6   7   8   9   10   11   12   13   14   15   ผลลัพธ์
  ---------------- --- --- --- --- --- --- --- --- --- ---- ---- ---- ---- ---- ---- -------------------------
  วางแผน                                                                             WiL proposal และวัตถุประสงค์

  ศึกษางานวิจัย                                                                         สรุปงานวิจัยที่เกี่ยวข้องกับระบบ
                                                                                     FBB

  เลือกอุปกรณ์                                                                          เลือกเซนเซอร์, MCU

  สั่งซื้อและทดลอง                                                                       สั่งซื้อและ Unit test
                                                                                     อุปกรณ์ที่สั่งมา

  ระบบสื่อสาร                                                                          low-latency bidirectional
                                                                                     ระหว่างรถและ PC

  ออกแบบ FFB                                                                         อัลกอริทึม force feedback

  ประกอบเซนเซอร์                                                                      ติดตั้งอุปกรณ์ต่างๆลงบนรถ

  รวมระบบ                                                                            รวมระบบ FFB
                                                                                     ทั้งหมดและทดลองการทำงาน

  แก้ไขปัญหา                                                                           ระบบ FFB ที่ทำงานได้บนรถบังคับ

  ทดสอบและรายงาน                                                                     ผลทดสอบ และรายงานฉบับสมบูรณ์
  ------------------------------------------------------------------------------------------------------------

# บทที่ 2 ทฤษฎี/งานวิจัย/การศึกษาที่เกี่ยวข้อง

ในการพัฒนาระบบ Force Feedback Steering System
จำเป็นต้องอาศัยความเข้าใจเชิงลึกเกี่ยวกับพลศาสตร์ของยานพาหนะและเทคนิคการประมวลผลข้อมูลจากเซนเซอร์
โดยสรุปงานวิจัยสำคัญที่สนับสนุนโครงงานได้ดังนี้:

## 2.1 แนวคิดพวงมาลัยเสมือนสำหรับ Force Feedback (Virtual Wheel Concept)

อ้างอิงจากงานวิจัยของ Balachandran, Erlien, และ Gerdes (2014) จาก Stanford
University ที่เสนอ \"Virtual Wheel Concept\" ซึ่งเป็นกรอบการทำงานสำหรับระบบ
Force Feedback ที่แบ่งแรงตอบสนองออกเป็น 2 ประเภทหลักตามคุณสมบัติทางกลไก:

### 2.1.1 แรงต้านทานแบบพาสซีฟ (Passive Resistive Forces)

เป็นแรงที่เพิ่มน้ำหนักและความหนืดของพวงมาลัยโดยไม่มีพลังงานอิสระในการหมุนพวงมาลัยด้วยตัวเอง
ประกอบด้วย:

1.  แรงหน่วง (Damping): แรงต้านเชิงวิสคัสที่แปรผันกับความเร็วเชิงมุมของพวงมาลัย

2.  แรงเสียดทาน (Friction): แรงต้านคงที่ในกลไกพวงมาลัย

3.  ความหนืดกลาง (Centering Stiffness): แรงคืนตัวเข้าสู่ศูนย์ที่แปรผันตามความเร็วรถ

### 2.1.2 แรงเชิงรุก (Active Restorative Forces)

เป็นแรงที่เกิดจากพลศาสตร์ยานพาหนะซึ่งสามารถหมุนพวงมาลัยได้โดยตรงแม้ผู้ขับขี่ปล่อยมือ:

1.  แรงคืนตัวจากยาง (Self-Aligning Torque):
    แรงที่ยางสร้างขึ้นเพื่อดึงพวงมาลัยกลับสู่ตำแหน่งสมดุล

2.  แรงโน้มถ่วง (Gravity Compensation): แรงที่เกิดขึ้นเมื่อรถอยู่บนพื้นผิวเอียง

3.  แรงสั่นสะเทือนพื้นผิว (Surface Jolt): แรงกระแทกความถี่สูงจากความขรุขระของถนน

## 2.2 สมการพื้นฐานของระบบ Force Feedback

จาก Balachandran et al. (2014) สมการหลักของระบบ Force Feedback คือ:

$$\tau_{FFB\ } = B \cdot \dot{\theta} + T_{fric} \cdot sgn(\theta ˙) + K_{stiff} \cdot \theta + \tau_{SAT} + \tau_{Gravity} + \tau_{Surface\_ Jolt}$$

โดยที่:

- $\tau_{FFB}$ = แรงบิดรวมที่ส่งไปยังพวงมาลัย

- $B$ = สัมประสิทธิ์การหน่วง (Damping coefficient)

- $\dot{\theta}$ = ความเร็วเชิงมุมของพวงมาลัย (rad/s)

- $T_{fric}$ = แรงเสียดทานคงที่

- $K_{stiff}$ = ค่าความแข็งของสปริงคืนตัว

- $\theta$ = มุมเลี้ยวของพวงมาลัย (rad)

- $\tau_{SAT}$ = แรงคืนตัว (Self-Aligning Torque)

- $\tau_{Gravity}$ = แรงชดเชยความโน้มถ่วง

- $\tau_{Surface\_ Jolt}$ = แรงสั่นสะเทือนจากพื้นผิว

## 2.3 ระบบ Virtual Vehicle สำหรับ Steer-by-Wire

Mehdizadeh และ Kabganian (2011) เสนอสถาปัตยกรรม \"Virtual Vehicle\"
ซึ่งใช้โมเดลทางคณิตศาสตร์ของยานพาหนะจริงในการคำนวณแรง Feedback
โดยแยกระบบพวงมาลัยออกจากระบบหลามล้อเพื่อเพิ่มประสิทธิภาพในการควบคุม

## 2.4 การประมาณค่าแรงจากยางและการตรวจจับการลื่นไถล

จาก IEEE 9568828 งานวิจัยเกี่ยวกับระบบ Teleoperated ที่ใช้ Slip Angle Estimation
สำหรับ Force Feedback ซึ่งใช้ข้อมูลจาก IMU
ในการประมาณแรงที่กระทำต่อยางและตรวจจับสถานะการลื่นไถล

## 2.5 การออกแบบระบบ Haptic Feedback สำหรับ Steering

Katzourakis, Abbink, และ Happee (2010) นำเสนอการออกแบบระบบ Force
Feedback สำหรับการทดลอง Human-Machine Interface
โดยใช้โมเดลทางกายภาพในการคำนวณแรงบิดที่เหมาะสม

## 2.6 การประเมินระบบ Steering ด้วย Haptic Feedback

Wang, Wang, และ Wagner (2018) เสนอวิธีการประเมินอุปกรณ์บังคับพวงมาลัยที่มี Haptic
Feedback สำหรับยานพาหนะกึ่ง-อัตโนมัติและอัตโนมัติ
โดยใช้ทั้งการวัดเชิงปริมาณและการประเมินจากผู้ใช้

# บทที่ 3 ระเบียบวิธีวิจัย

## 3.1 สถาปัตยกรรมระบบ

ระบบประกอบด้วย 3 ส่วนหลัก:

1.  ESP32-C6 ทำหน้าที่เป็นหน่วยรับ-ส่งข้อมูลเซนเซอร์และควบคุม Servo/ESC

2.  PC ทำหน้าที่คำนวณอัลกอริทึม FFB และส่งคำสั่งไปยังรถ

3.  เซนเซอร์ (IMU, Load Cell, Current Sensor) สำหรับวัดสถานะรถ

## 3.2 ฮาร์ดแวร์

### 3.2.1 รายละเอียดเซนเซอร์ที่ใช้

  ------------------------------------------------------------------------
  อุปกรณ์                   ขา GPIO                 หน้าที่
  ----------------------- ----------------------- ------------------------
  Current Sensor (ACS712) GPIO 4                  วัดกระแสไฟฟ้าของ Servo

  IMU (BNO086 V2)         I2C (0x4A)              วัดความเร่งและอัตราการหมุน

  Load Cell 1kg with      GPIO 5, 18              วัดแรงต้านในระบบบังคับเลี้ยว
  HX711                                           
  ------------------------------------------------------------------------

![](media/image2.jpeg){width="1.6in" height="0.8881277340332459in"}
![](media/image3.jpeg){width="1.5972222222222223in"
height="1.5972222222222223in"}

![](media/image4.jpeg){width="0.9in"
height="1.6in"}![](media/image5.jpeg){width="1.6in"
height="0.9044838145231846in"}

### 3.2.2 รายละเอียดรถบังคับวิทยุที่ใช้

  -----------------------------------------------------------------------
  รายการ                  รายละเอียด
  ----------------------- -----------------------------------------------
  MCU                     ESP32-C6

  Chassis                 1/10 Scale Chassis

  Drivetrain              All-Wheel Drive

  Motor                   Rocket RC BLDC 10.5T

  ESC                     Rocket RC 130A

  Servo                   9IMod 20 kg servo

  Battery                 2S LiPo 5200mAh

  Step down               LM2596
  -----------------------------------------------------------------------

![](media/image6.jpeg){width="2.686639326334208in" height="2.0in"}
![](media/image7.jpeg){width="1.7203313648293963in" height="2.0in"}

![](media/image8.jpeg){width="2.0in" height="1.125133420822397in"}
![](media/image9.jpeg){width="1.1258683289588802in" height="2.0in"}
![](media/image10.jpeg){width="2.0in" height="0.9689840332458443in"}
![](media/image11.jpeg){width="1.1258683289588802in" height="2.0in"}

![](media/image12.jpeg){width="2.8427384076990374in"
height="1.0277777777777777in"}

### 3.2.3 รายละเอียดอุปรณ์บังคับรถที่ใช้

  -----------------------------------------------------------------------
  รายการ                  รายละเอียด
  ----------------------- -----------------------------------------------
  Steering wheel          Thrustmaster T248

  Pedals                  Thrustmaster T3PM
  -----------------------------------------------------------------------

![](media/image13.jpeg){width="2.0193897637795275in" height="2.0in"}
![](media/image14.jpeg){width="1.736304680664917in" height="2.0in"}

## 3.3 ระบบการสื่อสาร

ระบบใช้ WiFi Access Point โดย ESP32-C6 ทำหน้าที่เป็น Access Point ชื่อ
\"ESP32-RC-CAR\" และใช้โปรโตคอล UDP พอร์ต 4210 สำหรับการสื่อสารแบบ
Low-latency

รูปแบบข้อมูล:

- PC → ESP32: S{steering 0-180} T{throttle -100 to 100}

- ESP32 → PC: A{accX},{accY},{accZ}G{gyroX},{gyroY},{gyroZ}L{loadCell}

## 3.4 อัลกอริทึมการคำนวณแรง Force Feedback

### 3.4.1 สูตรหลัก (จาก Balachandran et al., 2014)

จากแนวคิด Virtual Wheel Concept สมการแรงบิดรวมคือ:

$$\tau_{FFB} = \tau_{Passive\_ Resistive} + \tau_{Active\_ Restorative}$$

### 3.4.2 แรงต้านทานแบบพาสซีฟ (Passive Resistive)

$$\tau_{Passive\_ Resistive} = B \cdot \dot{\theta} + T_{fric} \cdot sgn\left( \dot{\theta} \right) + K_{stiff} \cdot \theta + \tau_{LoadCell}$$

  ----------------------------------------------------------------------------------------------------------------------------------
  พารามิเตอร์                              แหล่งข้อมูล        สูตร                            คำอธิบาย
  -------------------------------------- --------------- ------------------------------ --------------------------------------------
  $$B \cdot \dot{\theta}$$               Thrustmaster    $$\dot{\theta} \times Gain$$   แรงเสียดทานที่แปรผันตามความเร็วเชิงมุมพวงมาลัย
                                         T248 Encoder                                   

  $$T_{fric} \cdot sgn(\dot{\theta})$$   Thrustmaster    $$Gain \times (1 - v_{s})$$    แรงเสียดทานที่แปรผันตามความเร็วของรถ
                                         T248 Encoder                                   ($T_{fric} = K_{fric} \times (1 - v_{s})$)
                                                                                        โดย $v_{s}$ คือค่า Speed Factor ที่แปรผันจาก
                                                                                        Velocity estimate

  $$K_{stiff} \cdot \theta$$             Thrustmaster    $$\theta \times Gain$$         ความหนืดกลาง
                                         T248 Encoder +                                 ($K_{stiff} = 2000 + v_{s} \times 8000$)
                                         Velocity                                       ที่เพิ่มขึ้นตามความเร็วรถ
                                         Estimate(IMU)                                  

  $$\tau_{LoadCell}$$                    Loadcell        $$L \times Gain$$              แรงต้านจากกลไกการบังคับเลี้ยว
  ----------------------------------------------------------------------------------------------------------------------------------

การเพิ่ม Load Cell (Empirical Extension) จากงานวิจัยของ Karimi & Mann (2009)
เรื่อง \"Torque feedback on the steering wheel of agricultural vehicles\"
พบว่าแรงต้านในระบบบังคับเลี้ยว (Steering system resistance)
มีผลต่อความรู้สึกของผู้ขับขี่ งานวิจัยนี้ชี้ให้เห็นว่าแรงต้านจากกลไกการบังคับเลี้ยวเป็นส่วนหนึ่งของ
\"road feel\" ที่ช่วยให้ผู้ขับขี่รับรู้สถานะของยานพาหนะได้ดีขึ้น

ดังนั้นในการทดลองนี้ ระบบได้เพิ่ม Load Cell เพื่อวัดแรงต้านจริงในระบบบังคับเลี้ยว
โดยเพิ่มพจน์ Load Resistance เข้ากับสมการ

**หมายเหตุ:** พจน์ $\tau_{LoadCell}$ เป็นการขยายเชิงประจักษ์ (Empirical
extension) ที่ไม่ได้อยู่ในสมการต้นฉบับของ Balachandran et al. (2014)
แต่ได้รับแรงบันดาลใจจากการสังเกตของ Karimi & Mann (2009)
ที่ว่าแรงต้านในระบบบังคับเลี้ยวมีความสำคัญต่อความรู้สึกของผู้ขับขี่

### 3.4.3 แรงเชิงรุก (Active Restorative)

$$\tau_{Active\_ Restorative} = \tau_{SAT} + \tau_{Gravity} + \tau_{Surface\_ Jolt}$$

$$\tau_{Active\_ Restorative} = K_{center} \cdot \theta + a_{x} \cdot G_{x} + a_{z} \cdot G_{z\_ accel}$$

  -------------------------------------------------------------------------------------------------------------------
  **พารามิเตอร์**                   **แหล่งข้อมูล**                                         **คำอธิบาย**
  ------------------------------- -------------- ------------------------------------- ------------------------------
  $$K_{center} \cdot \theta$$     Thrustmaster   $$\theta \times v_{s} \times Gain$$   แรงคืนตัวเข้าศูนย์
                                  T248 Encoder +                                       
                                  Velocity                                             
                                  Estimate                                             

  $$a_{x} \cdot G_{x}$$           BNO086 (accX)  $$accX \times Gain$$                  แรงชดเชยความเอียงจากแรงโน้มถ่วง

  $$a_{z} \cdot G_{z\_ accel}$$   BNO086 (accZ)  $$accZ \times Gain$$                  แรงสั่นสะเทือนจากพื้นผิว
  -------------------------------------------------------------------------------------------------------------------

### 3.4.1 การประมาณความเร็ว (Velocity Estimation)

เนื่องจากไม่มีEncoder ที่ล้อ ความเร็วของรถจึงถูกประมาณจากการรวมค่าความเร่งในแนวแกน X
จาก IMU(BNO086) ด้วย Exponential decay:

$$\widehat{v} = 0.99 \cdot {\widehat{v}}_{prev} + 0.01 \cdot a_{x}
$$

โดยค่าน้ำหนัก 0.99 และ 0.01 ทำให้ความเร็ว estimate มีการเปลี่ยนแปลงช้า (Low-pass
filter effect) ป้องกันสัญญาณรบกวน

### 3.4.1 การตรวจจับการลื่นไถล (Drift Detection)

ตามวิธีการของ IEEE 9568828 ระบบตรวจจับการลื่นไถลโดยเปรียบเทียบความเร่งทางข้าง
(accY) กับค่า Threshold ที่ปรับตามความเร็ว:

$$\text{if~} \mid a_{y} \mid > \gamma \cdot (1 + \mid \widehat{v} \mid )\text{~then~}\tau_{Active\_ Restorative} \leftarrow 0.2 \cdot \tau_{Active\_ Restorative}$$

โดยที่ $\gamma = 3.0$ m/s² คือค่า Threshold พื้นฐาน เมื่อตรวจพบ Drift ระบบจะลด
Active torque ลง 80% ทันทีเพื่อให้ผู้ขับขี่รับรู้ถึงการสูญเสียการยึดเกาะ

# บทที่ 4 การทดลองและผลการทดลอง/วิจัย

## 4.1 วิธีการทดสอบประสิทธิภาพ

เพื่อให้การประเมินประสิทธิภาพของระบบเป็นไปอย่างครอบคลุม จึงได้กำหนดวิธีการทดสอบดังนี้:

### 4.1.1 Latency Test

วิธีการทดสอบอ้างอิงจาก IEEE 9568828 โดยใช้สคริปต์ Python วัดค่า Round Trip Time
(RTT) ผ่านโปรโตคอล UDP

ขั้นตอน:

1.  เปิด ESP32-C6 และรอให้ Access Point พร้อม

2.  เชื่อมต่อคอมพิวเตอร์ WiFi เข้ากับ ESP32-RC-CAR

3.  รัน python test_client.py (สคริปต์จะส่ง 100 แพ็กเกจอัตโนมัติ)

4.  บันทึกผลลงไฟล์ CSV

เกณฑ์ผ่าน: ค่าเฉลี่ย Latency \< 70 ms, Packet loss \< 1%

### 4.1.2 Range Test

ทดสอบความเสถียรของสัญญาณ WiFi ที่ระยะ 10-40 เมตร

ขั้นตอน:

1.  วางรถที่จุดเริ่มต้น เปิดเครื่อง

2.  เชื่อมต่อ WiFi และรัน test_client.py

3.  ขยับระยะทาง: 5ม., 10ม., 15ม., 20ม., 25ม., 30ม., 40ม., 50ม.

4.  บันทึกค่า Latency และ Packet Loss ที่แต่ละระยะ

เกณฑ์ผ่าน: ระยะ 20 เมตรขึ้นไป โดย Latency \< 70 ms และ Packet loss \< 5%

### 4.1.3 การทดสอบการทำงานของ Current Sensor (ACS712)

ทดสอบการทำงานเบื้องต้นของ ACS712 5A ในการวัดกระแสของ Servo

ขั้นตอน:

1.  เปิดระบบ จ่ายไฟ Servo

2.  สังเกตค่ากระแสจาก Serial Monitor ขณะ Servo หมุน

3.  ตรวจสอบว่าค่ากระแสเปลี่ยนแปลงเมื่อ Servo ทำงาน

เกณฑ์ผ่าน: ACS712 อ่านค่าได้และค่าเปลี่ยนแปลงตามการทำงานของ Servo

### 4.1.4 การทดสอบเพื่อ Calibrate Loadcell (HX711)

ทดสอบและสอบเทียบค่าจาก HX711 Load Cell โดยจำกัดน้ำหนักสูงสุดที่ 500g
เพื่อป้องกันความเสียหายของชิ้นส่วน RC

ขั้นตอน:

1.  ติดตั้ง Load Cell ที่ตำแหน่ง Steering Linkage

2.  วัดค่าเมื่อไม่มีแรงกด (Zero/Tare)

3.  ตั้งรถในท่าตั้งฉาก (Sideways) วางน้ำหนัก 100g, 200g, 300g, 400g, 500g
    บนพวงมาลัย (ซ้าย/ขวา) บันทึกค่า L

4.  หาความสัมพันธ์ระหว่างน้ำหนักจริงกับค่าที่วัดได้ เพื่อคำนวณ Scale Factor ใหม่

เกณฑ์ผ่าน: ค่า L ที่วัดได้มีความสัมพันธ์เชิงเส้นกับน้ำหนักที่รู้จัก และ Scale Factor
มีความแม่นยำไม่เกิน ±10%

### 4.1.5 การทดสอบองค์ประกอบ FFB (Component Validation)

ทดสอบการทำงานของแต่ละส่วนประกอบตามวิธีการของ Wang et al. (2018) และ Shakeri
et al. (2016)

4.1.5.1 ทดสอบการทำงานของ Damping Force

ขั้นตอน:

1.  หมุนพวงมาลัยที่ความเร็วต่างกัน (ช้า/เร็ว)

2.  บันทึก FFB

3.  ตรวจสอบ: FFB ∝ \|θ̇\|

4.1.5.2 ทดสอบการทำงานของ Friction Force

ขั้นตอน:

1.  หมุนพวงมาลัยที่ความเร็วคงที่

2.  บันทึก FFB

3.  ตรวจสอบ: Friction คงที่ไม่ขึ้นกับความเร็วเชิงมุม แต่ลดเมื่อ speed_factor เพิ่ม

4.1.5.3 ทดสอบการทำงานของ Steering Stiffness

ขั้นตอน:

1.  หมุนพวงมาลัยไปที่มุมต่างๆ

2.  บันทึก FFB

3.  ตรวจสอบ: \|FFB\| ∝ \|θ\| และทิศทางตรงข้ามการเคลื่อนที่

4.1.5.4 ทดสอบการทำงานของ Load Cell (Steering Resistance Measurement)

ขั้นตอน:

1.  บันทึกค่า L ขณะหมุนพวงมาลัย

2.  ตรวจสอบ: \|L\| ∝ \|θ\|

4.1.5.5 ทดสอบการทำงานของ Self Aligning Torque

ขั้นตอน:

1.  ปล่อยพวงมาลัยให้คืนตัวที่ความเร็วต่างกัน

2.  บันทึก FFB

3.  ตรวจสอบ: FFB ∝ \|θ\| × speed_factor

4.1.5.6 ทดสอบการทำงานของ Gravity Torque

ขั้นตอน:

1.  เอียงรถไปทางซ้าย-ขวา

2.  บันทึก FFB

3.  ตรวจสอบ: FFB ∝ accX

4.1.5.7 ทดสอบการทำงานของ Surface Jolt

ขั้นตอน:

1.  เขย่าตัวรถ

2.  บันทึก FFB

3.  ตรวจสอบ: \|FFB\| ∝ \|accZ\|

4.1.5.8 ทดสอบการทำงานของ Drift Detection

ขั้นตอน:

1.  ขับรถเป็นเส้นตรง → บันทึก accY และ FFB ปกติ

2.  ขับรถให้ล้อเสีย Traction → บันทึก FFB ลดลง

3.  ตรวจสอบ: เมื่อ \|accY\| \> threshold → FFB ลด 80%

### 4.1.6 การทดสอบเชิงปริมาณ (Quantitative Test)

บันทึกข้อมูล Telemetry ระหว่างการทดสอบเพื่อวิเคราะห์ความสัมพันธ์:

วิธีที่ 1: ยกรถ (Wheels-Free Simulation)

1.  ยกรถขึ้นให้ล้อหมุนอิสระ

2.  ปรับ Throttle เพื่อเพิ่มความเร็วที่ประมาณจาก accX integration

3.  หมุนพวงมาลัยที่ความเร็วต่างๆ (ช้า/กลาง/เร็ว)

4.  บันทึก FFB และ Telemetry

วิธีที่ 2: ขับรถในพื้นที่จำกัด

1.  ขับรถในห้อง/ทางเดิน

2.  บันทึก FFB และ Telemetry ขณะเลี้ยวกลับไปมา

## 4.2 ผลการทดลอง

### 4.2.1 Latency Test Results

จากการทดสอบความหน่วง (Latency Test) จำนวน 100 แพ็กเกจ ผลการทดลองเป็นดังนี้:

![Figure 1 ผลการทดลอง RRT Latency test](media/image15.png){width="6.5in"
height="2.5972222222222223in"}

- จำนวนแพ็กเกจ: 100 แพ็กเกจ

- อัตราการสูญเสียข้อมูล (Packet Loss): 0.00%

- ค่าเฉลี่ย (Mean): 5.20 ms

- ค่ามัธยฐาน (Median): 3.18 ms

- ค่าความเบี่ยงเบนมาตรฐาน (Std Dev): 5.54 ms

- ค่าต่ำสุด (Min): 1.00 ms

- ค่าสูงสุด (Max): 38.72 ms

- Percentile 95: 16.19 ms

- Percentile 99: 23.81 ms

**วิเคราะห์ผล:**
การทดลองแสดงให้เห็นว่าระบบสื่อสารไร้สายมีความเสถียรสูงและมีค่าความหน่วงเฉลี่ย 5.20 ms
ซึ่งต่ำกว่าเกณฑ์ที่กำหนดไว้ (70 ms) อย่างมาก การกระจายตัวของ Latency มี Median ที่
3.18 ms แสดงว่าค่าส่วนใหญ่อยู่ในช่วงต่ำ มีเพียงบางค่าเท่านั้นที่สูงขึ้น (Max 38.72 ms)
ซึ่งอาจเกิดจากการรบกวนของ WiFi ในช่วงสั้น

### 4.2.2 Range Test Results

ผลการทดสอบความเสถียรของสัญญาณ WiFi ที่ระยะต่างๆ โดยใช้ UDP ping test จำนวน 100
แพ็กเกจในแต่ละระยะ![](media/image16.png){width="5.5in"
height="3.14705927384077in"}![](media/image17.png){width="5.5in"
height="3.1470581802274715in"}

  -----------------------------------------------------------------------
       ระยะทาง (ม.)          Latency เฉลี่ย (ms)        Packet Loss (%)
  ----------------------- ----------------------- -----------------------
            10                     5.12                      0

            20                     5.24                      0

            30                     5.86                      0

            40                     7.43                      0
  -----------------------------------------------------------------------

**วิเคราะห์ผล:** ระบบสามารถรักษาความเสถียรได้ถึงระยะ 40 เมตร โดยมี Packet loss
0% และ Latency เฉลี่ยเพียง 7.43 ms ซึ่งต่ำกว่าเกณฑ์ 70 ms ที่กำหนดอย่างมาก ทั้ง 4
ระยะทดสอบผ่านเกณฑ์ทั้งหมด ระบบ WiFi UDP ของ ESP32-C6
มีความเสถียรสูงในระยะใกล้-กลาง ซึ่งเพียงพอต่อการใช้งานรถบังคับวิทยุในระยะสายตา

### 4.2.3 ผลการทดสอบการทำงานของ Current Sensor (ACS712)

การทดสอบแบ่งเป็น 2 ส่วน คือ กระแสตอน Idle (เซอร์โวอยู่กับที่) และกระแสตอน Sweep
(เซอร์โวหมุนซ้าย-ขวา) เพื่อตรวจสอบว่าสามารถแยกความแตกต่างของกระแสได้หรือไม่

![](media/image18.png){width="6.493055555555555in"
height="4.638888888888889in"}

  --------------------------------------------------------------
  Status         Average     S.D.        Min         Max
  -------------- ----------- ----------- ----------- -----------
  Idle           2.011 A     0.120 A     1.122 A     2.150 A

  Sweeping       2.140 A     0.255 A     1.231 A     3.069 A
  (moving)                                           

  Sweeping       2.032 A     0.143 A     1.183 A     2.428 A
  (Stationary)                                       
  --------------------------------------------------------------

**วิเคราะห์ผล:** ค่ากระแสระหว่าง Idle และ Moving มีการซ้อนทับกัน (Overlap) ที่ช่วง
1.77-3.07 A
ทำให้ไม่สามารถแยกแยะได้อย่างชัดเจนว่ากระแสที่วัดได้เกิดจากการเคลื่อนที่ของเซอร์โวหรือจาก
Noise/Spike ของตัวเซอร์โวเอง ค่า S.D. ของ Moving (0.255 A) สูงกว่า Idle
(0.120 A) เกือบ 2 เท่า แสดงว่า Noise
รบกวนมากเกินกว่าจะใช้เป็นตัวบ่งชี้การเคลื่อนไหวได้

### 4.2.4 ผลการทดสอบเพื่อ Calibrate Load Cell (HX711)

ติดน้ำหนักที่ปลายล้อหน้าในท่าตั้งฉากของรถบังคับทั้งซ้ายและขวาทีละด้าน

  ---------------------------------------------------------------------------------
  **น้ำหนัก**   **ซ้าย      **ขวา      **L Scale  **L Error    **R Scale  **R Error
              (L)**      (R)**      Factor**   from average Factor**   from average
                                               (%)**                   (%)**
  ----------- ---------- ---------- ---------- ------------ ---------- ------------
  100g        19,852     -22,897    198.5      -5.59        229.0      +9.92

  200g        46,214     -38,552    231.1      +5.71        192.8      -5.10

  300g        64,040     -59,288    213.5      +0.51        197.6      -2.62

  400g        81,603     -87,501    204.0      -2.75        218.8      +4.14

  500g        108,502    -101,204   217.0      +2.75        202.4      -0.76
  ---------------------------------------------------------------------------------

**Average: L Scale Factor = 211.0, R Scale Factor = 208.1**

**สูตรที่ได้:**

- ซ้าย (Left): $Scale\_ Factor_{L} = 211.0$

- ขวา (Right): $Scale\_ Factor_{R} = 208.1$

**วิเคราะห์ผล:** ค่า Scale Factor เฉลี่ย = 211.0 (ซ้าย) และ 208.1 (ขวา) Error
สูงสุด = 9.92% (ที่ 100g ขวา) ซึ่งใกล้เคียง ±10% จึงผ่านเกณฑ์

### 4.2.5 ผลการทดสอบองค์ประกอบ FFB (Component Validation)

4.2.5.1 ผลทดสอบการทำงานของ Damping Force

![](media/image19.png){width="6.493055555555555in"
height="4.638888888888889in"}

- แนวโน้ม: FFB เพิ่มขึ้นเมื่อ \|θ̇\| เพิ่มขึ้น

4.2.5.2 ผลทดสอบการทำงานของ Friction Force

![](media/image20.png){width="6.493055555555555in"
height="5.409722222222222in"}

- Friction สูงขณะเคลื่อนที่ (\|FFB\| ≈ 1800), ต่ำขณะหยุดนิ่ง (\|FFB\| ≈ 0)

- Friction ลดลงเมื่อ Speed Factor เพิ่มขึ้น

4.2.5.3 ผลทดสอบการทำงานของ Steering Stiffness

![](media/image21.png){width="6.493055555555555in"
height="2.1666666666666665in"}

- แนวโน้ม: \|FFB\| เพิ่มขึ้นเมื่อ \|θ\| เพิ่มขึ้น

- ทิศทางตรงข้ามกับการเคลื่อนที่

4.2.5.4 ผลทดสอบการทำงานของ Load Cell (Steering Resistance Measurement)

![](media/image22.png){width="6.493055555555555in"
height="2.1666666666666665in"}

- แนวโน้ม: \|L\| มีความสัมพันธ์เชิงเส้นกับมุมเลี้ยว

4.2.5.5 ผลทดสอบการทำงานของ Self Aligning Torque

![](media/image23.png){width="6.493055555555555in"
height="2.1666666666666665in"}

- แนวโน้ม: FFB เพิ่มขึ้นเมื่อ \|θ\| เพิ่มขึ้น

- FFB เพิ่มขึ้นเมื่อ Speed Factor สูงขึ้น

4.2.5.6 ผลทดสอบการทำงานของ Gravity

![](media/image24.png){width="6.493055555555555in"
height="4.638888888888889in"}

- แนวโน้ม: FFB ∝ accX

- ทิศทางขึ้นกับทิศทางการเอียง

4.2.5.7 ผลทดสอบการทำงานของ Surface Jolt

![](media/image25.png){width="6.493055555555555in"
height="4.638888888888889in"}

- แนวโน้ม: \|FFB\| ∝ \|accZ\|

4.2.5.8 ผลทดสอบการทำงานของ Drift Detection

![](media/image26.png){width="6.493055555555555in"
height="5.409722222222222in"}

- เมื่อ \|accY\| \< threshold: FFB ปกติ

- เมื่อ \|accY\| \> threshold: FFB ลดลง \~80%

### 4.2.6 ผลการทดสอบเชิงปริมาณ (Quantitative Test)

![](media/image27.png){width="6.493055555555555in"
height="5.194444444444445in"}

การประเมิน: ระบบ FFB ตอบสนองถูกต้องต่อทุกองค์ประกอบ (Damping, Friction,
Stiffness, Load, SAT, Gravity, Jolt, Drift)
และมีพฤติกรรมเป็นธรรมชาติเมื่อขับขี่จริง

# บทที่ 5 บทสรุป

## 5.1 สรุปผลการดำเนินงาน

ระบบ Force Feedback (FFB)
สำหรับรถบังคับวิทยุที่พัฒนาขึ้นในงานวิจัยนี้สามารถทำงานได้ตามวัตถุประสงค์ที่ตั้งไว้
โดยมีผลการทดสอบดังนี้:

**ผลการทดสอบหลัก:**

- ความหน่วง (Latency) เฉลี่ย 5.20 ms --- ต่ำกว่าเกณฑ์ 70 ms ที่กำหนดไว้อย่างมาก

- ระยะการสื่อสารไร้สาย 40 เมตร โดยไม่มี packet loss

- ระบบ Force Feedback ที่ทำงานได้อย่างเป็นธรรมชาติ

## 5.2 ความสำเร็จที่ได้รับ

1.  **ระบบสื่อสาร Low-latency** : ระบบ WiFi UDP บน ESP32-C6 สามารถส่งข้อมูล
    telemetry และรับคำสั่ง FFB ได้ในเวลาเฉลี่ย 5.20 ms ซึ่งต่ำกว่าเกณฑ์ที่กำหนดไว้ถึง
    13 เท่า

2.  **การปรับแต่งระบบเซนเซอร์** : พบว่า ACS712 Current Sensor
    ไม่เหมาะสมสำหรับวัดแรงบิดเซอร์โว เนื่องจาก noise สูงและ idle/moving overlap
    จึงใช้เพียง Load Cell และ IMU

3.  **Passive/Active Force** : สามารถจำลอง Passive force
    หรือก็คือแรงที่เพิ่มน้ำหนักและความหนืดของพวงมาลัย และจำลอง Active Force
    หรือก็คือสามารถหมุนพวงมาลัยได้โดยตรงแม้ผู้ขับขี่ปล่อยมือ บนพวงมาลัย Thrustmaster
    T248

4.  **อัลกอริทึม Force Feedback แบบครบถ้วน** : ระบบประกอบด้วยองค์ประกอบ FFB
    ทั้งหมด 8 ส่วนตาม Virtual Wheel Concept ของ Balachandran et al. (2014):

    - Passive: Damping, Friction, Passive Stiffness, Load Cell

    - Active: SAT, Gravity, Surface Jolt, Drift Detection

5.  **การจำลองพฤติกรรมการขับขี่** :
    ระบบสามารถจำลองพฤติกรรมการขับขี่ของมนุษย์ได้อย่างเป็นธรรมชาติ ทั้งการตอบสนองช้า
    การสั่นสะเทือน และการปรับตัวต่อสภาพถนน

## 5.3 ข้อจำกัด

1.  Current Sensor ACS712 5A มี noise สูงเกินไป และความแตกต่างของ
    idle/moving ต่ำไปทำให้ไม่สามารถแยกแยะสถานะ idle/moving ได้

2.  ตัวล็อก Load Cell เป็น 3d print part จึงทำให้มีการอ่อนตัวและคลายของสกรูยึด

3.  การทดสอบยังอยู่ในพื้นที่จำกัดและพื้นผิวแบบเดียว

## 5.4 แนวทางการพัฒนาในอนาคต

1.  เพิ่มสภาพแวดล้อมจริงการทดสอง โดยทดสอบระบบบนรถบังคับวิทยุในสภาพถนนต่างๆ

2.  ปรับปรุง Load Cell Calibration โดยเพิ่มจำนวนจุด calibration และใช้วิธี
    least-squares regression แทนการเฉลี่ยแบบง่าย

3.  เพิ่ม Adaptive Gain ปรับค่า gain
    อัตโนมัติตามพฤติกรรมผู้ขับขี่เพื่อให้ได้ความรู้สึกที่เหมาะสมที่สุด

4.  เพิ่ม Heading Correction ใช้ gyroZ (Yaw Rate)
    เพื่อชดเชยการเลี้ยวของรถเมื่อขับขี่ตรง

5.  ปรับปรุง Drift Detection เพิ่มเงื่อนไขจาก yaw rate เพื่อป้องกัน false positive
    และปรับให้การ scale แรงเป็นแบบ adaptive ตามสถานะของรถ

# เอกสารอ้างอิง

\[1\] A. Balachandran, S. M. Erlien, and J. C. Gerdes, \"The virtual
wheel concept for supportive steering feedback during active steering
interventions,\" in ASME Dynamic Systems and Control Conference, 2014.
(Virtual Wheel Concept --- สูตรหลักของ FFB)

\[2\] E. Mehdizadeh and M. Kabganian, \"A new force feedback for
steer-by-wire vehicles via virtual vehicle concept,\" in 50th IEEE
Conference on Decision and Control, 2011, pp. 6160-6165. (Virtual
Vehicle architecture)

\[3\] IEEE 9568828: \"Remote driving testbed with force feedback based
on slip angle estimation.\" (การประมาณ Slip angle และ Drift Detection)

\[4\] D. I. Katzourakis, D. A. Abbink, and R. Happee, \"Steering force
feedback for human--machine-interface automotive experiments,\" IEEE
Transactions on Haptics, vol. 3, no. 4, pp. 225-237, 2010. (Haptic
steering system design)

\[5\] C. Wang, Y. Wang, and J. R. Wagner, \"Evaluation of alternative
steering devices with adjustable haptic feedback for semi-autonomous and
autonomous vehicles,\" SAE International Journal of Connected and
Automated Vehicles, vol. 1, no. 2, 2018. (Haptic steering device
evaluation methodology)

\[6\] G. Shakeri, S. A. Brewster, and J. Williamson, \"Evaluating haptic
feedback on a steering wheel in a simulated driving scenario,\" in
Proceedings of the 2016 CHI Conference on Human Factors in Computing
Systems, 2016, pp. 206-217. (Likert scale steering evaluation)

\[7\] M. Böhle, B. Schick, and S. Müller, \"Steering feedback in dynamic
driving simulators: The influence of steering wheel vibration and
vehicle motion frequency,\" IEEE Transactions on Intelligent Vehicles,
vol. 9, no. 3, pp. 1045-1056, 2024. (Steering feedback testing protocol)

\[8\] Q. Guo, D. Zhao, et al., \"Active suspension control strategy of
multi-axle emergency rescue vehicle based on inertial measurement
unit,\" Sensors, vol. 21, no. 4, p. 1256, 2021. (IMU-based control and
sensor fusion)

\[9\] S. Du, J. Wang, et al., \"Improving observability of an inertial
system by rotary motions of an IMU,\" IEEE Transactions on
Instrumentation and Measurement, vol. 66, no. 11, pp. 3082-3090, 2017.
(Sensor fusion for drift reduction)

\[10\] T. D. Gillespie, Fundamentals of Vehicle Dynamics. Society of
Automotive Engineers (SAE), 1992. (พลศาสตร์ยานพาหนะพื้นฐาน)

\[11\] H. Mohellebi and A. Kheddar, \"Adaptive haptic feedback steering
wheel for driving simulators,\" IEEE Transactions on Vehicular
Technology, vol. 58, no. 2, pp. 660-671, 2009. (Adaptive haptic
feedback)

\[12\] D. Karimi and D. Mann, \"Torque feedback on the steering wheel of
agricultural vehicles,\" Computers and Electronics in Agriculture, vol.
65, no. 1, pp. 77-84, 2009. (Steering system resistance และ road feel)
