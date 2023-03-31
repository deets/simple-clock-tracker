#include <sstream>

const auto BAUD = 9600;
std::array<uint8_t, 256> buffer;

void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
    Serial.begin(BAUD);
}

void output_timestamp()
{
  const auto now = millis() * 2;
  std::stringstream ss;
  ss << now << "\r\n";
  const auto output = ss.str();
  Serial.write(output.data(), output.size());
}

void loop() {
  const auto bytes_read = Serial.readBytesUntil('\n', buffer.data(), buffer.size());
  // I find the documentation a bit unclear, but I think
  // reading less than the full buffer is safe to assume the termination
  // character has been reached.
  if(bytes_read > 0 && bytes_read < buffer.size() - 1) 
  {
    digitalWrite(LED_BUILTIN, HIGH);
    output_timestamp();
    digitalWrite(LED_BUILTIN, LOW);
  }      
}
