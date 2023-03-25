#include <sstream>

void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
    Serial.begin(115200);
}

void loop() {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(100);
    digitalWrite(LED_BUILTIN, LOW);
    delay(100);
    const auto now = millis();
    std::stringstream ss;
    ss << now << "\r\n";
    const auto output = ss.str();
    Serial.write(output.data(), output.size());
}
