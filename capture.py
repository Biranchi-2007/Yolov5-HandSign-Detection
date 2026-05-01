import cv2
import os

# Path to save captured images
save_path = r"C:\Users\dbira\yolov5\dataset\images\train"

# Create folder if it doesn't exist
os.makedirs(save_path, exist_ok=True)

# Ask user for the class name once
class_name = input("input")

# Open webcam (0 = default camera)
cap = cv2.VideoCapture(0)

count = 0
print("Press SPACE to capture an image, ESC to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Show the live videoC60
    cv2.imshow("Capture Photos", frame)

    key = cv2.waitKey(1)

    if key % 256 == 27:  # ESC key
        print("Exiting...")
        break
    elif key % 256 == 32:  # SPACE key
        # Auto-generate filename with class name + counter
        img_name = os.path.join(save_path, f"{class_name}_{count}.jpg")
        cv2.imwrite(img_name, frame)
        print(f"Saved: {img_name}")
        count += 1

# Release resources
cap.release()
cv2.destroyAllWindows()


#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <UniversalTelegramBot.h>
#include <ArduinoJson.h>

// ── WiFi Credentials ──────────────────────────
#define WIFI_SSID     "IOT"
#define WIFI_PASSWORD "1234567890"

// ── Telegram Bot ──────────────────────────────
#define BOT_TOKEN  "8569020974:AAHs__YU9929E9GKUnQvXhX8g0Bcq060vzo"
#define CHAT_ID    "-5178830589"

WiFiClientSecure secured_client;
UniversalTelegramBot bot(BOT_TOKEN, secured_client);

// ── LCD ───────────────────────────────────────
LiquidCrystal_I2C lcd(0x27, 16, 2);

// ── Flex Sensor Pins ──────────────────────────
#define FLEX1 34  // INDEX
#define FLEX2 35  // MIDDLE
#define FLEX3 32  // RING
#define FLEX4 33  // LITTLE

// ── Baselines ─────────────────────────────────
#define INDEX_BASE     1000
#define MIDDLE_BASE    673
#define RING_BASE      10
#define LITTLE_BASE    10

// ── Thresholds ────────────────────────────────
#define INDEX_BENT_THRESHOLD   (INDEX_BASE    + 50)
#define MIDDLE_BENT_THRESHOLD  (MIDDLE_BASE   + 50)
#define RING_BENT_THRESHOLD    (RING_BASE     + 10)
#define LITTLE_BENT_THRESHOLD  (LITTLE_BASE   + 10)

// ── State Tracking ────────────────────────────
String lastGesture       = "";
bool   telegramSentForThisGesture = false;  // KEY FLAG

// ─────────────────────────────────────────────
void printSeparator() {
  Serial.println("================================");
}

void showOnLCD(String line1, String line2) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(line1);
  lcd.setCursor(0, 1);
  lcd.print(line2);
}

void sendTelegram(String message) {
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("  [TELEGRAM] Sending: " + message);
    bool sent = bot.sendMessage(CHAT_ID, message, "");
    if (sent) {
      Serial.println("  [TELEGRAM] Sent OK! Will NOT send again until gesture changes.");
    } else {
      Serial.println("  [TELEGRAM] Send FAILED!");
    }
  } else {
    Serial.println("  [TELEGRAM] WiFi not connected!");
  }
}

void detectAndDisplay(bool index, bool middle, bool ring, bool little,
                      int f1, int f2, int f3, int f4)
{

  String gesture     = "";
  String msg1        = "";
  String msg2        = "";
  String telegramMsg = "";

  if (!index && !middle && !ring && !little)    //(!index && !middle && !ring && !little)
  {
    gesture     = "ALL OPEN";
    msg1        = "I AM OK ";
    msg2        = "ALL OPEN"; 
  } 
  else if (index && !middle && !ring && !little)
  {
    gesture     = "COME HERE";
    msg1        = " COME HERE  ";
    msg2        = " PLEASE    ";
    telegramMsg = "Please come here 🆘!";
  } 
  else if (!index && middle && !ring && !little)
  {
    gesture     = "PAIN";
    msg1        = " I AM FEELING  ";
    msg2        = " PAIN    ";
    telegramMsg = "I am feeling some PAIN 🤒";
  } 
 else if (!index && !middle && ring && !little)
  {
    gesture     = "I NEED FOOD";
    msg1        = " I NEED  ";
    msg2        = " FOOD    ";
    telegramMsg = "I am feeling hungry! 🍽️ I need FOOD!";
  } 
else if (!index && !middle && !ring && little)
  {
    gesture     = "I NEED WATER";
    msg1        = " I NEED  ";
    msg2        = " WATER    ";
    telegramMsg = "I am feeling thirsty, please bring water 💧!";
  }
else if (index && middle && !ring && !little)
  {
    gesture     = "FEELING GOOD";
    msg1        = " I AM FEELING  ";
    msg2        = " GOOD    ";
    telegramMsg = "I am feeling good, ALL OKAY! Need Some rest 😴";
  }
else if (!index && middle && ring && !little)
  {
    gesture     = "I NEED MEDICINE";
    msg1        = " I NEED  ";
    msg2        = " MY MEDICINE    ";
    telegramMsg = "Hey It's time for my MEDICINE 💊";
  }
else if (!index && !middle && ring && little)
  {
    gesture     = "I NEED TO GO WASHROOM";
    msg1        = " I NEED TO GO";
    msg2        = " TO WASHROOM    ";
    telegramMsg = "Hey I need to go to WASHROOM!";
  }
else if (index && !middle && !ring && little)
  {
    gesture     = "I NEED CHANGE POSITION";
    msg1        = " I NEED TO ";
    msg2        = " CHANGE POSITION    ";
    telegramMsg = "Help! I need to change position!";
  }   
else if (!index && middle && ring && little)
  {
    gesture     = "UNEASE";
    msg1        = " I AM UNABLE TO  ";
    msg2        = " BREATH    ";
    telegramMsg = "I am feeling uneasy, DIFFICULTY IN BREATHING!";
  }  
else if (index && middle && ring && !little)
  {
    gesture     = "FEELING HOT/COLD";
    msg1        = " I AM FEELING  ";
    msg2        = " HOT/COLD HERE    ";
    telegramMsg = "Increase/Decrease the temperature of A/C!";
  }  
else if (index && middle && ring && little)
  {
    gesture     = "PANIC";
    msg1        = " I AM SICK ";
    msg2        = " CALL DOCTOR    ";
    telegramMsg = "I am SICK! Call the DOCTOR 🏥 Immediately!";
  }  
else 
  {
    gesture     = "UNKNOWN";
    msg1        = "UNKNOWN ";
    msg2        = "GESTURE ";
    telegramMsg = "";
  }

  // ── Serial Monitor ────────────────────────────
  printSeparator();
  Serial.println("     FLEX SENSOR MONITOR");
  printSeparator();
  Serial.printf("  Index  [F1]: %4d  | Threshold > %4d | %s\n",
                f1, INDEX_BENT_THRESHOLD,  index  ? "BENT" : "OPEN");
  Serial.printf("  Middle  [F2]: %4d  | Threshold > %4d | %s\n",
                f2, MIDDLE_BENT_THRESHOLD,  middle  ? "BENT" : "OPEN");
  Serial.printf("  Ring [F3]: %4d  | Threshold > %4d | %s\n",
                f3, RING_BENT_THRESHOLD, ring ? "BENT" : "OPEN");
  Serial.printf("  Little   [F4]: %4d  | Threshold > %4d | %s\n",
                f4, LITTLE_BENT_THRESHOLD,   little   ? "BENT" : "OPEN");
  printSeparator();

  // ── NEW Gesture detected ──────────────────────
  if (gesture != lastGesture) {
    Serial.println("  >> NEW GESTURE DETECTED <<");
    Serial.println("  GESTURE  : " + gesture);
    Serial.println("  LCD LINE1: [" + msg1 + "]");
    Serial.println("  LCD LINE2: [" + msg2 + "]");

    lastGesture = gesture;
    telegramSentForThisGesture = false;  // reset flag for new gesture
    showOnLCD(msg1, msg2);
  }

  // ── Send Telegram ONCE only ───────────────────
  if (!telegramSentForThisGesture && telegramMsg != "") {
    sendTelegram(telegramMsg);
    telegramSentForThisGesture = true;   // 🔒 LOCK — no more sends until gesture changes
    Serial.println("  [TELEGRAM] LOCKED until next gesture change.");
  } else if (telegramSentForThisGesture) {
    Serial.println("  [TELEGRAM] Already sent for this gesture. Waiting for change...");
  }

  printSeparator();
  Serial.println();
}

// ─────────────────────────────────────────────
void setup() {
  Serial.begin(115200);
  delay(1000);

  lcd.init();
  lcd.backlight();
  showOnLCD("  FLEX SENSOR  ", "  STARTING...  ");

  printSeparator();
  Serial.println("  Connecting to WiFi: " + String(WIFI_SSID));
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  secured_client.setCACert(TELEGRAM_CERTIFICATE_ROOT);

  showOnLCD("  WiFi...      ", "  Please wait  ");
  int attempt = 0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    attempt++;
    if (attempt > 40) {
      Serial.println("\n  WiFi FAILED! Offline Mode.");
      showOnLCD("  WiFi FAILED  ", "  Offline Mode ");
      delay(2000);
      break;
    }
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n  WiFi Connected!");
    Serial.println("  IP: " + WiFi.localIP().toString());
    showOnLCD("  WiFi OK!     ", WiFi.localIP().toString());
    delay(1500);
    bot.sendMessage(CHAT_ID, "✅ Flex Sensor System Online!", "");
    Serial.println("  Startup Telegram sent!");
  }

  printSeparator();
  Serial.println("  ESP32 FLEX SENSOR + TELEGRAM");
  printSeparator();
  Serial.printf("  Index  nominal: %4d | BENT when > %4d\n", INDEX_BASE,  INDEX_BENT_THRESHOLD);
  Serial.printf("  Middle  nominal: %4d | BENT when > %4d\n", MIDDLE_BASE,  MIDDLE_BENT_THRESHOLD);
  Serial.printf("  Ring nominal: %4d | BENT when > %4d\n", RING_BASE, RING_BENT_THRESHOLD);
  Serial.printf("  Little   nominal: %4d | BENT when > %4d\n", LITTLE_BASE,   LITTLE_BENT_THRESHOLD);
  printSeparator();

  showOnLCD("  FLEX SENSOR  ", "   READY...    ");
  delay(1500);
  lcd.clear();
  Serial.println("  System Ready!");
  Serial.println();
}

// ─────────────────────────────────────────────
void loop() {
  int f1 = analogRead(FLEX1);
  int f2 = analogRead(FLEX2);
  int f3 = analogRead(FLEX3);
  int f4 = analogRead(FLEX4);

  bool thumb  = f1 > INDEX_BENT_THRESHOLD;
  bool index  = f2 > MIDDLE_BENT_THRESHOLD;
  bool middle = f3 > RING_BENT_THRESHOLD;
  bool ring   = f4 > LITTLE_BENT_THRESHOLD;

  detectAndDisplay(thumb, index, middle, ring, f1, f2, f3, f4);

  delay(1000);
}
