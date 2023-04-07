#include <sstream>

const int MILLIS_FACTOR = 2;

const int INPUT_PIN = 21;

std::array<uint8_t, 256> buffer;

unsigned long button_presses[256];
uint8_t button_presses_read;
uint8_t button_presses_write;
void record_button_press() {
  button_presses[button_presses_write++] = millis() * MILLIS_FACTOR;
}

void setup() {
  Serial.begin(115200);  
  button_presses_read = button_presses_write = 0;
  pinMode(LED_BUILTIN, OUTPUT);
  attachInterrupt(digitalPinToInterrupt(INPUT_PIN), record_button_press, FALLING);
}

void output_timestamp()
{
  const auto now = millis() * MILLIS_FACTOR;
  std::stringstream ss;
  ss << now << "\r\n";
  const auto output = ss.str();
  Serial.write(output.data(), output.size());
}

void output_button_presses()
{
  std::stringstream ss;
  
  while(button_presses_read != button_presses_write)
  {
    ss << "b " << button_presses[button_presses_read++] << "\r\n";
    const auto output = ss.str();
    Serial.write(output.data(), output.size());
    ss.clear();
  }
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
  output_button_presses();
}
