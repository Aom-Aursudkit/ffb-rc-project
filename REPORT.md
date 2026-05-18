# รายงานโครงงาน: ระบบ Force Feedback สำหรับรถบังคับวิทยุ

## สารบัญ
1. [บทที่ 1 บทนำ](#บทที่-1-บทนำ)
2. [บทที่ 2 ทฤษฎีและงานวิจัยที่เกี่ยวข้อง](#บทที่-2-ทฤษฎีและงานวิจัยที่เกี่ยวข้อง)
3. [บทที่ 3 ระเบียบวิธีวิจัย](#บทที่-3-ระเบียบวิธีวิจัย)
4. [บทที่ 4 การทดลองและผลการทดลอง](#บทที่-4-การทดลองและผลการทดลอง)
5. [บทที่ 5 บทสรุป](#บทที่-5-บทสรุป)
6. [เอกสารอ้างอิง](#เอกสารอ้างอิง)

---

## บทที่ 1 บทนำ

### 1.1 ที่มาและความสำคัญ
รถบังคับวิทยุ (RC cars) ในปัจจุบันมักใช้ตัวส่งสัญญาณแบบ Pistol-grip ซึ่งขาดการตอบสนองเชิงฟิสิกส์ (Physical feedback) ไปยังผู้ขับขี่ ผู้ขับขี่ได้รับเพียงข้อมูลทางสายตา (Visual feedback) ทำให้ขาดความสมจริงและไม่สามารถรับรู้พฤติกรรมของรถได้โดยตรง ระบบ Force Feedback (FFB) จึงถูกนำมาใช้เพื่อถ่ายทอดแรงตอบสนองจากตัวรถไปยังผู้ขับขี่ผ่านพวงมาลัย

### 1.2 ปัญหางานวิจัย
ระบบพวงมาลัยตอบสนองแรงสำหรับรถบังคับวิทยุยังมีข้อจำกัดด้านความหน่วง (Latency) และความสมจริงของแรงตอบสนอง เนื่องจากขาดการประมวลผลพลศาสตร์ของยานพาหนะแบบ Real-time

### 1.3 ผลผลิตและผลลัพธ์ (Outputs and Outcomes)

**ผลผลิต (Outputs)**
1. ระบบพวงมาลัยตอบสนองแรง (Force Feedback Steering System) สำหรับรถบังคับวิทยุขนาด 1:10
2. เฟิร์มแวร์ ESP32-C6 สำหรับรับ-ส่งข้อมูลเซนเซอร์และควบคุม Servo/ESC
3. แอปพลิเคชัน PC (pc_wheel.py) สำหรับคำนวณอัลกอริทึม FFB และส่งคำสั่งไปยังรถ

**ผลลัพธ์ (Outcomes)**
1. ผู้ขับขี่สามารถรับรู้พฤติกรรมของรถผ่านแรงตอบสนองบนพวงมาลัย
2. ระบบมีความหน่วงต่ำกว่า 70 ms และระยะการสื่อสารไร้สายอย่างน้อย 20 เมตร
3. การควบคุมรถบังคับวิทยุมีความสมจริงมากขึ้น

### 1.4 ความต้องการของระบบ
- ความหน่วง (Latency) ต่ำกว่า 70 ms
- ระยะการสื่อสารไร้สายอย่างน้อย 20 เมตร
- แรงตอบสนอง (Torque) แปรผันได้ตามพฤติกรรมรถ

### 1.5 ขอบเขตของงาน
- ออกแบบระบบ FFB บนพวงมาลัย Sim Racing Wheel
- ใช้ IMU (BNO086) และ Load Cell ในการประมวลผลแรงตอบสนอง
- ดำเนินการในขอบเขต Steering-geometry-based force feedback

### 1.6 ข้อกำหนด
สมมติว่าตำแหน่งพวงมาลัยตรงกับตำแหน่งล้อหน้าเนื่องจาก Servo มีความเร็วเพียงพอ

---

---

## บทที่ 2 ทฤษฎีและงานวิจัยที่เกี่ยวข้อง

### 2.1 แนวคิดพวงมาลัยเสมือนสำหรับ Force Feedback (Virtual Wheel Concept)
อ้างอิงจากงานวิจัยของ Balachandran, Erlien, และ Gerdes (2014) จาก Stanford University ที่เสนอ "Virtual Wheel Concept" ซึ่งเป็นกรอบการทำงานสำหรับระบบ Force Feedback ที่แบ่งแรงตอบสนองออกเป็น 2 ประเภทหลักตามคุณสมบัติทางกลไก:

#### 2.1.1 แรงต้านทานแบบพาสซีฟ (Passive Resistive Forces)
เป็นแรงที่เพิ่มน้ำหนักและความหนืดของพวงมาลัยโดยไม่มีพลังงานอิสระในการหมุนพวงมาลัยด้วยตัวเอง ประกอบด้วย:

- **แรงหน่วง (Damping):** แรงต้านเชิงวิสคัสที่แปรผันกับความเร็วเชิงมุมของพวงมาลัย
- **แรงเสียดทาน (Friction):** แรงต้านคงที่ในกลไกพวงมาลัย
- **ความหนืดกลาง (Centering Stiffness):** แรงคืนตัวเข้าสู่ศูนย์ที่แปรผันตามความเร็วรถ

#### 2.1.2 แรงเชิงรุก (Active Restorative Forces)
เป็นแรงที่เกิดจากพลศาสตร์ยานพาหนะซึ่งสามารถหมุนพวงมาลัยได้โดยตรงแม้ผู้ขับขี่ปล่อยมือ:

- **แรงคืนตัวจากยาง (Self-Aligning Torque):** แรงที่ยางสร้างขึ้นเพื่อดึงพวงมาลัยกลับสู่ตำแหน่งสมดุล
- **แรงโน้มถ่วง (Gravity Compensation):** แรงที่เกิดขึ้นเมื่อรถอยู่บนพื้นผิวเอียง
- **แรงสั่นสะเทือนพื้นผิว (Surface Jolt):** แรงกระแทกความถี่สูงจากความขรุขระของถนน

### 2.2 สมการพื้นฐานของระบบ Force Feedback
จาก Balachandran et al. (2014) สมการหลักของระบบ Force Feedback คือ:

$$\tau_{FFB} = B \cdot \dot{\theta} + T_{fric} \cdot \text{sgn}(\dot{\theta}) + K_{stiff} \cdot \theta + \tau_{SAT} + \tau_{Gravity} + \tau_{Surface\_Jolt}$$

โดยที่:
- $\tau_{FFB}$ = แรงบิดรวมที่ส่งไปยังพวงมาลัย
- $B$ = สัมประสิทธิ์การหน่วง (Damping coefficient)
- $\dot{\theta}$ = ความเร็วเชิงมุมของพวงมาลัย (rad/s)
- $T_{fric}$ = แรงเสียดทานคงที่
- $K_{stiff}$ = ค่าความแข็งของสปริงคืนตัว
- $\theta$ = มุมเลี้ยวของพวงมาลัย (rad)
- $\tau_{SAT}$ = แรงคืนตัวจากยาง (Self-Aligning Torque)
- $\tau_{Gravity}$ = แรงชดเชยความโน้มถ่วง
- $\tau_{Surface\_Jolt}$ = แรงสั่นสะเทือนจากพื้นผิว

### 2.3 งานวิจัยที่เกี่ยวข้อง

#### 2.3.1 ระบบ Virtual Vehicle สำหรับ Steer-by-Wire
Mehdizadeh และ Kabganian (2011) เสนอสถาปัตยกรรม "Virtual Vehicle" ซึ่งใช้โมเดลทางคณิตศาสตร์ของยานพาหนะจริงในการคำนวณแรง Feedback โดยแยกระบบพวงมาลัยออกจากระบบหลามล้อเพื่อเพิ่มประสิทธิภาพในการควบคุม

#### 2.3.2 การประมาณค่าแรงจากยางและการตรวจจับการลื่นไถล
จาก IEEE 9568828 งานวิจัยเกี่ยวกับระบบ Teleoperated ที่ใช้ Slip Angle Estimation สำหรับ Force Feedback ซึ่งใช้ข้อมูลจาก IMU ในการประมาณแรงที่กระทำต่อยางและตรวจจับสถานะการลื่นไถล

#### 2.3.3 การออกแบบระบบ Haptic Feedback สำหรับ Steering
Katzourakis, Abbink, และ Happee (2010) นำเสนอการออกแบบระบบ Force Feedback สำหรับการทดลอง Human-Machine Interface โดยใช้โมเดลทางกายภาพในการคำนวณแรงบิดที่เหมาะสม

#### 2.3.4 การประเมินระบบ Steering ด้วย Haptic Feedback
Wang, Wang, และ Wagner (2018) เสนอวิธีการประเมินอุปกรณ์บังคับพวงมาลัยที่มี Haptic Feedback สำหรับยานพาหนะกึ่ง-อัตโนมัติและอัตโนมัติ โดยใช้ทั้งการวัดเชิงปริมาณและการประเมินจากผู้ใช้

### 2.4 การรวมข้อมูลเซนเซอร์ (Sensor Fusion)
Du et al. (2017) เสนอเทคนิคการปรับปรุงการสังเกตการณ์ของระบบ Inertial โดยใช้การหมุนของ IMU เองเพื่อลดความคลาดเคลื่อน (Drift & Bias) ของเซนเซอร์

---

## บทที่ 3 ระเบียบวิธีวิจัย

### 3.1 สถาปัตยกรรมระบบ
ระบบประกอบด้วย 3 ส่วนหลัก:
1. **ESP32-C6** ทำหน้าที่เป็นหน่วยรับ-ส่งข้อมูลเซนเซอร์และควบคุม Servo/ESC
2. **PC (pc_wheel.py)** ทำหน้าที่คำนวณอัลกอริทึม FFB และส่งคำสั่งไปยังรถ
3. **เซนเซอร์** (IMU, Load Cell, Current Sensor) สำหรับวัดสถานะรถ

### 3.2 ฮาร์ดแวร์

#### 3.2.1 รายละเอียดฮาร์ดแวร์หลัก
| อุปกรณ์ | ขา GPIO | หน้าที่ |
|---------|---------|---------|
| Servo Motor | GPIO 15 | ควบคุมมุมเลี้ยวล้อหน้า |
| ESC | GPIO 23 | ควบคุมความเร็วมอเตอร์ |
| NeoPixel LED | GPIO 8 | แสดงสถานะระบบ |
| Current Sensor (ACS712) | GPIO 4 | วัดกระแสไฟฟ้าของ Servo |
| IMU (BNO086 V2) | I2C (0x4A) | วัดความเร่งและอัตราการหมุน |
| Load Cell (HX711) | GPIO 5, 18 | วัดแรงต้านในระบบบังคับเลี้ยว |

#### 3.2.2 การติดตั้งเซนเซอร์
IMU (BNO086 V2) ติดตั้งที่จุดศูนย์กลางของตัวรถ (Geometric Center) เพื่อลดสัญญาณรบกวนจากแรงเหวี่ยง (Centrifugal noise)

#### 3.2.3 รายละเอียดรถบังคับวิทยุที่ใช้
| รายการ | รายละเอียด |
|--------|-----------|
| **แชสซี** | แชสซี 1/10 Scale (ไม่ระบุชื่อ) |
| **ระบบขับเคลื่อน** | All-Wheel Drive (AWD) |
| **มอเตอร์** | Sensored BLDC 10.5T (Rocket RC) |
| **ESC** | Rocket RC 130A (พร้อมสาย Sensor) |
| **เซอร์โว** | 9IMod 20 kg high-torque servo |
| **แบตเตอรี่** | 2S LiPo 5200mAh |

### 3.3 ระบบการสื่อสาร

ระบบใช้ **WiFi Access Point** (Mode: AP) โดย ESP32-C6 ทำหน้าที่เป็น Access Point ชื่อ "ESP32-RC-CAR" รหัสผ่าน "12345678" และใช้โปรโตคอล **UDP** พอร์ต **4210** สำหรับการสื่อสารแบบ Low-latency

รูปแบบข้อมูล:
- **PC → ESP32:** `S{steering 0-180} T{throttle -100 to 100}`
- **ESP32 → PC:** `A{accX},{accY},{accZ}G{gyroX},{gyroY},{gyroZ}L{loadCell}`

### 3.4 อัลกอริทึมการคำนวณแรง Force Feedback

#### 3.4.1 สูตรหลัก (จาก Balachandran et al., 2014)
จากแนวคิด Virtual Wheel Concept สมการแรงบิดรวมคือ:

$$\tau_{FFB} = \tau_{Passive\_Resistive} + \tau_{Active\_Restorative}$$

โดยสามารถเขียนแยกได้ดังนี้:

$$\tau_{FFB} = \underbrace{B \cdot \dot{\theta} + T_{fric} \cdot \text{sgn}(\dot{\theta}) + K_{stiff} \cdot \theta + \tau_{LoadCell}}_{\text{Passive Resistive}} + \underbrace{K_{center} \cdot \theta + a_x \cdot G_x + a_z \cdot G_{z\_accel}}_{\text{Active Restorative}}$$

**ความแตกต่างจากสูตรเดิมของ Balachandran:**
- สูตรเดิม: $K_{stiff} \cdot \theta$ อยู่ในส่วน Active (เป็นแรงคืนตัว)
- สูตรใหม่: แบ่ง $K_{stiff}$ ออกเป็น 2 ส่วน
  - **Passive Stiffness ($K_{stiff} = 500$):** ต้านการเบี่ยงเบนจากศูนย์ ทำให้เบี้ยงมาลัย "หนัก" ขึ้นเมื่อหมุนออกจากศูนย์
  - **Active Stiffness ($K_{center} = 20000$):** แรงคืนตัวเข้าศูนย์ที่เพิ่มขึ้นตามความเร็ว (Self-Aligning Torque)

#### 3.4.2 แรงต้านทานแบบพาสซีฟ (Passive Resistive)

$$\tau_{Passive\_Resistive} = B \cdot \dot{\theta} + T_{fric} \cdot \text{sgn}(\dot{\theta}) + K_{stiff} \cdot \theta + \tau_{LoadCell}$$

| พารามิเตอร์ | แหล่งข้อมูล | สูตร | คำอธิบาย |
|-------------|-------------|------|----------|
| $B \cdot \dot{\theta}$ | Thrustmaster T248 Encoder | $\dot{\theta} \times 2000$ | แรงหน่วงเชิงวิสคัส ต้านการหมุนเร็ว |
| $T_{fric} \cdot \text{sgn}(\dot{\theta})$ | Thrustmaster T248 Encoder | $2000 \times (1 - v_s)$ | แรงเสียดทานคงที่ แปรผกผันกับความเร็ว (โดย $v_s$ คือ Speed Factor) |
| $K_{stiff} \cdot \theta$ | Thrustmaster T248 Encoder + Velocity Estimate | $\theta \times 500$ | แรงต้านการเบี่ยงเบนจากศูนย์ |
| $\tau_{LoadCell}$ | Load Cell | $L \times 2000$ | แรงต้านจริงจากกลไกการบังคับเลี้ยว |

**การเพิ่ม Load Cell (Empirical Extension)**
จากงานวิจัยของ Karimi & Mann (2009) เรื่อง "Torque feedback on the steering wheel of agricultural vehicles" พบว่าแรงต้านในระบบบังคับเลี้ยว (Steering system resistance) มีผลต่อความรู้สึกของผู้ขับขี่ งานวิจัยนี้ชี้ให้เห็นว่าแรงต้านจากกลไกการบังคับเลี้ยวเป็นส่วนหนึ่งของ "road feel" ที่ช่วยให้ผู้ขับขี่รับรู้สถานะของยานพาหนะได้ดีขึ้น

ดังนั้นในการทดลองนี้ ระบบได้เพิ่ม Load Cell เพื่อวัดแรงต้านจริงในระบบบังคับเลี้ยว โดยเพิ่มพจน์ Load Resistance เข้ากับสมการ

**หมายเหตุ:** พจน์ $\tau_{LoadCell}$ เป็นการขยายเชิงประจักษ์ (Empirical extension) ที่ไม่ได้อยู่ในสมการต้นฉบับของ Balachandran et al. (2014) แต่ได้รับแรงบันดาลใจจากการสังเกตของ Karimi & Mann (2009)

#### 3.4.3 แรงเชิงรุก (Active Restorative)

$$\tau_{Active\_Restorative} = K_{center} \cdot \theta + a_x \cdot G_x + a_z \cdot G_{z\_accel}$$

| พารามิเตอร์ | แหล่งข้อมูล | สูตร | คำอธิบาย |
|-------------|-------------|------|----------|
| $K_{center} \cdot \theta$ | Thrustmaster T248 Encoder + Velocity Estimate | $\theta \times v_s \times 20000$ | แรงคืนตัวเข้าศูนย์ (เพิ่มขึ้นตามความเร็ว) |
| $a_x \cdot G_x$ | BNO086 (accX) | $accX \times 1500$ | แรงชดเชยความเอียงจากแรงโน้มถ่วง |
| $a_z \cdot G_{z\_accel}$ | BNO086 (accZ) | $accZ \times 500$ | แรงสั่นสะเทือนจากพื้นผิว |

### 3.5 การเชื่อมโยงเซนเซอร์กับสูตร

| เซนเซอร์ | ข้อมูลที่วัด | สูตรที่ใช้ | Gain |
|----------|-------------|-----------|------|
| Thrustmaster T248 Encoder | มุมพวงมาลัย ($\theta$) | $K_{stiff} \cdot \theta$ (Passive), $\tau_{SAT}$ (Active) | 500, 20000 |
| Thrustmaster T248 Encoder | ความเร็วเชิงมุม ($\dot{\theta}$) | $B \cdot \dot{\theta}$, $T_{fric} \cdot \text{sgn}(\dot{\theta})$ | 2000, 2000 |
| HX711 Load Cell | แรงต้านในระบบบังคับเลี้ยว ($L$) | $K_{load} \cdot L$ | 2000 |
| BNO086 (accX) | ความเร่งในแนวแกน X | $a_x \cdot G_x$ (Gravity) | 1500 |
| BNO086 (accY) | ว่าความเร่งในแนวแกน Y | Drift Detection | 3.0 (threshold) |
| BNO086 (accZ) | ความเร่งในแนวแกน Z | $a_z \cdot G_z$ (Surface Jolt) | 500 |
| BNO086 (Gyroscope) | gyroZ (Yaw Rate) | Drift Detection | - |

---

## บทที่ 4 การทดลองและผลการทดลอง

### 4.1 วิธีการทดสอบ

#### 4.1.1 การทดสอบความหน่วง (Latency Test)
วิธีการทดสอบอ้างอิงจาก IEEE 9568828 โดยใช้สคริปต์ Python (`test_client.py`) วัดค่า Round Trip Time (RTT) ผ่านโปรโตคอล UDP

**ขั้นตอน:**
1. เปิด ESP32-C6 และรอให้ Access Point พร้อม
2. เชื่อมต่อคอมพิวเตอร์เข้ากับ ESP32-RC-CAR
3. รัน `python test_client.py` (ส่ง 100 แพ็กเกจ)
4. บันทึกผลลงไฟล์ CSV

**เกณฑ์ผ่าน:** ค่าเฉลี่ย Latency < 70 ms, Packet loss < 1%

#### 4.1.2 การทดสอบระยะการส่งสัญญาณ (Range Test)
ทดสอบความเสถียรของสัญญาณ WiFi ที่ระยะ 5-50 เมตร

**ขั้นตอน:**
1. วางรถที่จุดเริ่มต้น เปิดเครื่อง
2. เชื่อมต่อ WiFi และรัน `test_client.py`
3. ขยับระยะทาง: 5ม., 10ม., 15ม., 20ม., 25ม., 30ม., 40ม., 50ม.
4. บันทึกค่า Latency และ Packet Loss ที่แต่ละระยะ

**เกณฑ์ผ่าน:** ระยะ 20 เมตรขึ้นไป โดย Latency < 70 ms และ Packet loss < 5%

#### 4.1.3 การทดสอบการทำงานของ Current Sensor (ACS712)
ทดสอบการทำงานเบื้องต้นของ ACS712 5A ในการวัดกระแสของ Servo

**ขั้นตอน:**
1. เปิดระบบ จ่ายไฟ Servo
2. สังเกตค่ากระแสจาก Serial Monitor ขณะ Servo หมุน
3. ตรวจสอบว่าค่ากระแสเปลี่ยนแปลงเมื่อ Servo ทำงาน

**เกณฑ์ผ่าน:** ACS712 อ่านค่าได้และค่าเปลี่ยนแปลงตามการทำงานของ Servo

#### 4.1.4 การทดสอบเพื่อหาสูตร Scale Factor ของ Load Cell (HX711)
ทดสอบเพื่อหาค่า Scale Factor สำหรับ HX711 Load Cell โดยจำกัดน้ำหนักสูงสุดที่ 500g เพื่อป้องกันความเสียหายของชิ้นส่วน RC

**ขั้นตอน:**
1. ติดตั้ง Load Cell ที่ตำแหน่ง Steering Linkage
2. วัดค่าเมื่อไม่มีแรงกด (Zero/Tare)
3. ตั้งรถในท่าตั้งฉาก (Sideways) วางน้ำหนัก 100g, 200g, 300g, 400g, 500g บนพวงมาลัย (ซ้าย/ขวา) บันทึกค่า L
4. หาความสัมพันธ์ระหว่างน้ำหนักจริงกับค่าที่วัดได้ เพื่อคำนวณ Scale Factor ใหม่

**เกณฑ์ผ่าน:** ค่า L ที่วัดได้มีความสัมพันธ์เชิงเส้นกับน้ำหนักที่รู้จัก และ Scale Factor มีความแม่นยำไม่เกิน ±10%

#### 4.1.5 การทดสอบองค์ประกอบ FFB (Component Validation)
วิธีการทดสอบอ้างอิงจาก:
- Wang et al. (2018) — วิธีการประเมินอุปกรณ์ haptic steering
- Shakeri et al. (2016) — การประเมิน haptic feedback บนพวงมาลัย
- Katzourakis et al. (2010) — การทดสอบด้วย inertia-spring-damper systems
- Gualino et al. (2006) — วิธีทดสอบ steering feeling แบบ objective

การทดสอบแบ่งเป็น **2 ประเภท:**

| ประเภท | วัตถุประสงค์ | ตัวชี้วัด |
|--------|-------------|----------|
| Component Test | ทดสอบแต่ละส่วนประกอบแยกกัน | แนวโน้มเชิงเส้น (Proportional) |
| System Test | ทดสอบระบบรวม | Lane position, Steering reversals |

**ตารางสรุป FFB Components ทั้งหมด:**

| # | ส่วนประกอบ | สูตร | Gain |
|---|-----------|------|------|
| 1 | Damping (Passive) | $B \cdot \dot{\theta}$ | 2000 |
| 2 | Friction (Passive) | $T_{fric} \cdot \text{sgn}(\dot{\theta})$ | 2000 |
| 3 | Passive Stiffness (Passive) | $K_{stiff} \cdot \theta \cdot \text{sgn}(\dot{\theta})$ | 500 |
| 4 | Load Cell (Passive) | $K_{load} \cdot L \cdot \text{sgn}(\dot{\theta})$ | 2000 |
| 5 | SAT (Active) | $K_{center} \cdot \theta$ | 20000 |
| 6 | Gravity (Active) | $a_x \cdot G_x$ | 1500 |
| 7 | Surface Jolt (Active) | $a_z \cdot G_z$ | 500 |

**4.1.5.1 การทดสอบ Component แบบง่าย (ตาม Katzourakis et al., 2010)**

วิธีการ: บันทึก FFB ขณะกระตุ้นแต่ละ component แยกกัน แล้ววิเคราะห์แนวโน้ม

**ทดสอบ Damping:**
1. หมุนพวงมาลัยที่ความเร็วต่างกัน (ช้า/เร็ว)
2. บันทึก FFB
3. ตรวจสอบ: FFB ∝ |θ̇|

**ทดสอบ Friction:**
1. หมุนพวงมาลัยที่ความเร็วคงที่
2. บันทึก FFB
3. ตรวจสอบ: Friction คงที่ไม่ขึ้นกับความเร็วเชิงมุม แต่ลดเมื่อ speed_factor เพิ่ม

**ทดสอบ Passive Stiffness:**
1. หมุนพวงมาลัยไปที่มุมต่างๆ
2. บันทึก FFB
3. ตรวจสอบ: |FFB| ∝ |θ| และทิศทางตรงข้ามการเคลื่อนที่

**ทดสอบ Load Cell:**
1. บันทึกค่า L ขณะหมุนพวงมาลัย
2. ตรวจสอบ: |L| ∝ |θ|

**ทดสอบ SAT:**
1. ปล่อยพวงมาลัยให้คืนตัวที่ความเร็วต่างกัน
2. บันทึก FFB
3. ตรวจสอบ: FFB ∝ |θ| × speed_factor

**ทดสอบ Gravity:**
1. เอียงรถไปทางซ้าย-ขวา
2. บันทึก FFB
3. ตรวจสอบ: FFB ∝ accX

**ทดสอบ Surface Jolt:**
1. เขย่าตัวรถ
2. บันทึก FFB
3. ตรวจสอบ: |FFB| ∝ |accZ|

**ทดสอบ Drift Detection:**
1. ขับรถเป็นเส้นตรง → บันทึก accY และ FFB ปกติ
2. หมุนพวงมาลัยกะทันหัน → บันทึก FFB ลดลง
3. ตรวจสอบ: เมื่อ |accY| > threshold → FFB ลด 80%

**4.1.5.2 System Test แบบง่าย (ตาม Toffin et al., 2007)**

**ทดสอบการขับขี่ในเส้นตรง:**
1. ขับรถตรง 10 เมตร
2. วัด lane position deviation
3. บันทึก steering reversal count

**ทดสอบการเลี้ยว:**
1. ขับรถเลี้ยว 90°
2. วัด settling time ของพวงมาลัย
3. บันทึก overshoot

#### 4.1.6 การทดสอบเชิงปริมาณ (Quantitative Test)
บันทึกข้อมูล Telemetry ระหว่างการทดสอบเพื่อวิเคราะห์ความสัมพันธ์:

**วิธีที่ 1: ยกรถ (Wheels-Free Simulation)**
1. ยกรถขึ้นให้ล้อหมุนอิสระ
2. ปรับ Throttle เพื่อเพิ่มความเร็วที่ประมาณจาก accX integration
3. หมุนพวงมาลัยที่ความเร็วต่างๆ (ช้า/กลาง/เร็ว)
4. บันทึก FFB และ Telemetry

**วิธีที่ 2: ขับรถในพื้นที่จำกัด**
1. ขับรถในห้อง/ทางเดิน
2. บันทึก FFB และ Telemetry ขณะเลี้ยวกลับไปมา

### 4.2 ผลการทดลอง

#### 4.2.1 ผลการทดสอบความหน่วง (Latency Test Results)
จากการทดสอบความหน่วง (Latency Test) จำนวน 100 แพ็กเกจ ผลการทดลองเป็นดังนี้:

| พารามิเตอร์ | ค่า |
|-------------|-----|
| จำนวนแพ็กเกจ | 100 |
| อัตราการสูญเสียข้อมูล (Packet Loss) | 0.00% |
| ค่าเฉลี่ย (Mean) | 5.20 ms |
| ค่ามัธยฐาน (Median) | 3.18 ms |
| ค่าความเบี่ยงเบนมาตรฐาน (Std Dev) | 5.54 ms |
| ค่าต่ำสุด (Min) | 1.00 ms |
| ค่าสูงสุด (Max) | 38.72 ms |
| Percentile 95 (P95) | 16.19 ms |
| Percentile 99 (P99) | 23.81 ms |

ผลการทดลองแสดงให้เห็นว่าระบบสื่อสารไร้สายมีความเสถียรสูงและมีค่าความหน่วงเฉลี่ย **5.20 ms** ซึ่งต่ำกว่าเกณฑ์ที่กำหนดไว้ (70 ms) อย่างมาก การกระจายตัวของ Latency มี Median ที่ 3.18 ms แสดงว่าค่าส่วนใหญ่อยู่ในช่วงต่ำ มีเพียงบางค่าเท่านั้นที่สูงขึ้น (Max 38.72 ms) ซึ่งอาจเกิดจากการรบกวนของ WiFi ในช่วงสั้น

**กราฟผลการทดสอบ:** ดูได้ที่ `Plotter/plot_result/`
- `latency_timeseries.png` — Latency ของแต่ละแพ็กเกจ
- `latency_histogram.png` — การกระจายตัวของค่า Latency
- `latency_boxplot.png` — Box plot แสดง Outlier
- `latency_cdf.png` — Cumulative Distribution Function

#### 4.2.2 ผลการทดสอบระยะการส่งสัญญาณ
ผลการทดสอบความเสถียรของสัญญาณ WiFi ที่ระยะต่างๆ โดยใช้ UDP ping test จำนวน 100 แพ็กเกจในแต่ละระยะ ข้อมูลจาก `data/range_results.csv`

| ระยะทาง (ม.) | Latency เฉลี่ย (ms) | Packet Loss (%) | ผ่าน/ไม่ผ่าน |
|:---:|:---:|:---:|:---:|
| 10 | 5.12 | 0.00 | ผ่าน |
| 20 | 5.24 | 0.00 | ผ่าน |
| 30 | 5.86 | 0.00 | ผ่าน |
| 40 | 7.43 | 0.00 | ผ่าน |

**วิเคราะห์ผล:** ระบบสามารถรักษาความเสถียรได้ถึงระยะ **40 เมตร** โดยมี Packet loss 0% และ Latency เฉลี่ยเพียง 7.43 ms ซึ่งต่ำกว่าเกณฑ์ 70 ms ที่กำหนดอย่างมาก ทั้ง 4 ระยะทดสอบผ่านเกณฑ์ทั้งหมด ระบบ WiFi UDP ของ ESP32-C6 มีความเสถียรสูงในระยะใกล้-กลาง ซึ่งเพียงพอต่อการใช้งานรถบังคับวิทยุในระยะสายตา

#### 4.2.3 ผลการทดสอบการทำงานของ Current Sensor (ACS712)

การทดสอบแบ่งเป็น 2 ส่วน คือ กระแสตอน Idle (เซอร์โวอยู่กับที่) และกระแสตอน Sweep (เซอร์โวหมุนซ้าย-ขวา) เพื่อตรวจสอบว่าสามารถแยกความแตกต่างของกระแสได้หรือไม่

| สถานะ | ค่าเฉลี่ย | S.D. | Min | Max | ช่วง (Range) |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **Idle (เซอร์โวอยู่กับที่)** | 2.011 A | 0.120 A | 1.122 A | 2.150 A | 1.028 A |
| **Sweep Moving (กำลังหมุน)** | 2.140 A | 0.255 A | 1.231 A | 3.069 A | 1.838 A |
| **Sweep Stationary (หยุดนิ่ง)** | 2.032 A | 0.143 A | 1.183 A | 2.428 A | 1.245 A |

**กราฟ:** ![Current Comparison](../Plotter/current_comparison.png)

**วิเคราะห์ผล:** ไม่ผ่าน — ค่ากระแสระหว่าง Idle และ Moving มีการซ้อนทับกัน (Overlap) ที่ช่วง 1.77-3.07 A ทำให้ไม่สามารถแยกแยะได้อย่างชัดเจนว่ากระแสที่วัดได้เกิดจากการเคลื่อนที่ของเซอร์โวหรือจาก Noise/Spike ของตัวเซอร์โวเอง ค่า S.D. ของ Moving (0.255 A) สูงกว่า Idle (0.120 A) เกือบ 2 เท่า แสดงว่า Noise รบกวนมากเกินกว่าจะใช้เป็นตัวบ่งชี้การเคลื่อนไหวได้

**ข้อสรุป:** Current Sensor (ACS712 5A) ไม่เหมาะสำหรับใช้วัดแรงบิดของเซอร์โวในโปรเจคนี้ เนื่องจาก:
1. ค่า Noise สูง (S.D. = 0.12-0.26 A) คิดเป็น ~10% ของ Full Scale (5A)
2. กระแส Idle กับ Moving มี Overlap ทำให้แยกไม่ได้
3. ควรใช้ Load Cell แทนในการวัดแรงบิดของพวงมาลัย

#### 4.2.4 ผลการทดสอบเพื่อหาสูตร Scale Factor ของ Load Cell (HX711)
วางน้ำหนักบนพวงมาลัยในท่าตั้งฉาก (Sideways) โดยใช้ HX711 Load Cell 1kg

| น้ำหนัก | ซ้าย (L) | ขวา (R) | L Scale Factor | L Error (%) | R Scale Factor | R Error (%) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 100g | 19,852 | -22,897 | 198.5 | -5.59 | 229.0 | +9.92 |
| 200g | 46,214 | -38,552 | 231.1 | +5.71 | 192.8 | -5.10 |
| 300g | 64,040 | -59,288 | 213.5 | +0.51 | 197.6 | -2.62 |
| 400g | 81,603 | -87,501 | 204.0 | -2.75 | 218.8 | +4.14 |
| 500g | 108,502 | -101,204 | 217.0 | +2.75 | 202.4 | -0.76 |
| **Average** | | | **211.0** | | **208.1** | |

**สูตรที่ได้:**
- ซ้าย (Left): $Scale\_Factor_L = 211.0$
- ขวา (Right): $Scale\_Factor_R = 208.1$

**วิเคราะห์ผล:** [ผ่าน/ไม่ผ่าน] — ค่า Scale Factor เฉลี่ย = 211.0 (ซ้าย) และ 208.1 (ขวา) Error สูงสุด = 9.92% (ที่ 100g ขวา) ซึ่งใกล้เคียง ±10% จึงผ่านเกณฑ์

#### 4.2.5 ผลการทดสอบองค์ประกอบ FFB

**4.2.5.1 Damping (Passive)**

**กราฟ:** ![Damping](../Plotter/ffb_plots/damping.png)

**ผลการวิเคราะห์:** [ผ่าน/ไม่ผ่าน]
- แนวโน้ม: FFB เพิ่มขึ้นเมื่อ |θ̇| เพิ่มขึ้น ✓/✗
- Damping Coefficient B = [ค่า] (Expected: 2000)

**4.2.5.2 Friction (Passive)**

**กราฟ:** ![Friction](../Plotter/ffb_plots/friction.png)

**ผลการวิเคราะห์:** [ผ่าน/ไม่ผ่าน]
- Friction คงที่ไม่ขึ้นกับความเร็วเชิงมุม ✓/✗
- Friction ลดลงเมื่อ Speed Factor เพิ่มขึ้น (T_fric = 2000 × (1 - v_s)) ✓/✗

**4.2.5.3 Passive Stiffness (Passive)**

**กราฟ:** ![Passive Stiffness](../Plotter/ffb_plots/stiffness_passive.png)

**ผลการวิเคราะห์:** [ผ่าน/ไม่ผ่าน]
- แนวโน้ม: |FFB| เพิ่มขึ้นเมื่อ |θ| เพิ่มขึ้น ✓/✗
- ทิศทางตรงข้ามกับการเคลื่อนที่ ✓/✗
- Gain = [ค่า] (Expected: 500)

**4.2.5.4 Load Cell (Passive)**

**กราฟ:** ![Load Cell](../Plotter/ffb_plots/loadcell.png)

**ผลการวิเคราะห์:** [ผ่าน/ไม่ผ่าน]
- แนวโน้ม: |L| เพิ่มขึ้นเมื่อ |θ| เพิ่มขึ้น ✓/✗
- L มีเครื่องหมายตามทิศทางการหมุน ✓/✗
- Gain = [ค่า] (Expected: 2000)

**4.2.5.5 SAT / Self-Centering (Active)**

**กราฟ:** ![SAT](../Plotter/ffb_plots/sat.png)

**ผลการวิเคราะห์:** [ผ่าน/ไม่ผ่าน]
- แนวโน้ม: FFB เพิ่มขึ้นเมื่อ |θ| เพิ่มขึ้น ✓/✗
- FFB เพิ่มขึ้นเมื่อ Speed Factor สูงขึ้น ✓/✗
- Gain = [ค่า] (Expected: 20000)

**4.2.5.6 Gravity (Active)**

**กราฟ:** ![Gravity](../Plotter/ffb_plots/gravity.png)

**ผลการวิเคราะห์:** [ผ่าน/ไม่ผ่าน]
- แนวโน้ม: FFB ∝ accX ✓/✗
- ทิศทางขึ้นกับทิศทางการเอียง ✓/✗
- Gain = [ค่า] (Expected: 1500)

**4.2.5.7 Surface Jolt (Active)**

**กราฟ:** ![Surface Jolt](../Plotter/ffb_plots/surface_jolt.png)

**ผลการวิเคราะห์:** [ผ่าน/ไม่ผ่าน]
- แนวโน้ม: Jolt ∝ |accZ| ✓/✗
- Gain G_z = [ค่า] (Expected: 500)

**4.2.5.8 Drift Detection**

**กราฟ:** ![Drift Detection](../Plotter/ffb_plots/drift_detection.png)

**ผลการวิเคราะห์:** [ผ่าน/ไม่ผ่าน]
- เมื่อ |accY| < threshold: FFB ปกติ ✓/✗
- เมื่อ |accY| > threshold: FFB ลดลง ~80% ✓/✗
- Threshold ที่ใช้ = [ค่า] (Expected: 3.0 × (1+|v|))

#### 4.2.6 สรุปผลการทดสอบโดยรวม

| # | รายการทดสอบ | สถานะ | หมายเหตุ |
|:---:|:---|:---:|:---|
| 1 | Latency Test | ⬜ รอทดสอบ | |
| 2 | Range Test 20m+ | ⬜ รอทดสอบ | |
| 3 | ACS712 Current Sensor | ⬜ ไม่ผ่าน | Noise สูงเกินไป |
| 4 | Load Cell Calibration | ⬜ รอทดสอบ | |
| 5 | FFB: Damping | ⬜ รอทดสอบ | |
| 6 | FFB: Friction | ⬜ รอทดสอบ | |
| 7 | FFB: Passive Stiffness | ⬜ รอทดสอบ | |
| 8 | FFB: Load Cell | ⬜ รอทดสอบ | |
| 9 | FFB: SAT | ⬜ รอทดสอบ | |
| 10 | FFB: Gravity | ⬜ รอทดสอบ | |
| 11 | FFB: Surface Jolt | ⬜ รอทดสอบ | |
| 12 | FFB: Drift Detection | ⬜ รอทดสอบ | |
| 13 | Subjective Test | ⬜ รอทดสอบ | |
| 14 | Quantitative Test | ⬜ รอทดสอบ | |

---

## บทที่ 5 บทสรุป
*[ส่วนนี้จะสรุปหลังจากเสร็จสิ้นการทดสอบ]*

---

## เอกสารอ้างอิง

[1] A. Balachandran, S. M. Erlien, and J. C. Gerdes, "The virtual wheel concept for supportive steering feedback during active steering interventions," in *ASME Dynamic Systems and Control Conference*, 2014. (Virtual Wheel Concept — สูตรหลักของ FFB)

[2] E. Mehdizadeh and M. Kabganian, "A new force feedback for steer-by-wire vehicles via virtual vehicle concept," in *50th IEEE Conference on Decision and Control*, 2011, pp. 6160-6165. (Virtual Vehicle architecture)

[3] IEEE 9568828: "Remote driving testbed with force feedback based on slip angle estimation." (การประมาณ Slip angle และ Drift Detection)

[4] D. I. Katzourakis, D. A. Abbink, and R. Happee, "Steering force feedback for human–machine-interface automotive experiments," *IEEE Transactions on Haptics*, vol. 3, no. 4, pp. 225-237, 2010. (Haptic steering system design)

[5] C. Wang, Y. Wang, and J. R. Wagner, "Evaluation of alternative steering devices with adjustable haptic feedback for semi-autonomous and autonomous vehicles," *SAE International Journal of Connected and Automated Vehicles*, vol. 1, no. 2, 2018. (Haptic steering device evaluation methodology)

[6] G. Shakeri, S. A. Brewster, and J. Williamson, "Evaluating haptic feedback on a steering wheel in a simulated driving scenario," in *Proceedings of the 2016 CHI Conference on Human Factors in Computing Systems*, 2016, pp. 206-217. (Likert scale steering evaluation)

[7] M. Böhle, B. Schick, and S. Müller, "Steering feedback in dynamic driving simulators: The influence of steering wheel vibration and vehicle motion frequency," *IEEE Transactions on Intelligent Vehicles*, vol. 9, no. 3, pp. 1045-1056, 2024. (Steering feedback testing protocol)

[8] Q. Guo, D. Zhao, et al., "Active suspension control strategy of multi-axle emergency rescue vehicle based on inertial measurement unit," *Sensors*, vol. 21, no. 4, p. 1256, 2021. (IMU-based control and sensor fusion)

[9] S. Du, J. Wang, et al., "Improving observability of an inertial system by rotary motions of an IMU," *IEEE Transactions on Instrumentation and Measurement*, vol. 66, no. 11, pp. 3082-3090, 2017. (Sensor fusion for drift reduction)

[10] T. D. Gillespie, *Fundamentals of Vehicle Dynamics*. Society of Automotive Engineers (SAE), 1992. (พลศาสตร์ยานพาหนะพื้นฐาน)

[11] H. Mohellebi and A. Kheddar, "Adaptive haptic feedback steering wheel for driving simulators," *IEEE Transactions on Vehicular Technology*, vol. 58, no. 2, pp. 660-671, 2009. (Adaptive haptic feedback)

[12] D. Karimi and D. Mann, "Torque feedback on the steering wheel of agricultural vehicles," *Computers and Electronics in Agriculture*, vol. 65, no. 1, pp. 77-84, 2009. (Steering system resistance และ road feel)