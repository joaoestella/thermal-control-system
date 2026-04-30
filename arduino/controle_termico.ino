// ============================================================
//  CONTROLE DE LÂMPADA COM PWM SIMULADO — FIAP
//  Pino do Relé : 2  (LOW = liga, HIGH = desliga)
//  Pino do Sensor: A0 (LM35 → 10 mV/°C)
// ============================================================

const int RELE_PIN   = 2;
const int SENSOR_PIN = A0;

// --- Configuração do ciclo PWM ---
const unsigned long PERIODO_MS = 30000UL; // 30 segundos

// --- Estado global ---
int  porcentagem    = 0;
bool releEstado     = false;
unsigned long inicioCiclo  = 0;
unsigned long ultimaLeitura = 0;

// --- Buffer serial simples (evita parseInt) ---
String bufferSerial = "";

void setup() {
  pinMode(RELE_PIN, OUTPUT);
  digitalWrite(RELE_PIN, HIGH); // Começa desligado
  Serial.begin(9600);
  inicioCiclo   = millis();
  ultimaLeitura = millis();
}

void loop() {
  unsigned long agora = millis();

  // ── 1. LEITURA SERIAL (não-bloqueante) ────────────────────
  while (Serial.available() > 0) {
    char c = (char)Serial.read();

    if (c == '\n') {
      bufferSerial.trim();
      if (bufferSerial.length() > 0) {
        int novo = bufferSerial.toInt();
        if (novo >= 0 && novo <= 100) {
          porcentagem = novo;
          inicioCiclo = agora;   // reinicia ciclo com novo valor
        }
      }
      bufferSerial = "";
    } else {
      bufferSerial += c;
    }
  }

  // ── 2. ENVIO DE TEMPERATURA (1 Hz, não-bloqueante) ────────
  if (agora - ultimaLeitura >= 1000UL) {
    ultimaLeitura = agora;
    int raw = analogRead(SENSOR_PIN);
    // LM35: Vout = 10 mV/grau → (raw * 5.0 / 1023) * 100
    float temp = (raw * 5.0 / 1023.0) * 100.0;
    Serial.println(temp, 1);  // ex: "27.3"
  }

  // ── 3. CONTROLE PWM (não-bloqueante) ──────────────────────
  unsigned long decorrido = agora - inicioCiclo;

  if (decorrido >= PERIODO_MS) {
    inicioCiclo = agora;
    decorrido   = 0;
  }

  bool deveLinkar;
  if (porcentagem >= 100) {
    deveLinkar = true;
  } else if (porcentagem <= 0) {
    deveLinkar = false;
  } else {
    unsigned long tempoLigado = (unsigned long)((porcentagem / 100.0) * PERIODO_MS);
    deveLinkar = (decorrido < tempoLigado);
  }

  // Aciona relé só quando o estado muda
  if (deveLinkar != releEstado) {
    releEstado = deveLinkar;
    digitalWrite(RELE_PIN, releEstado ? LOW : HIGH);
    // LOW  → relé fechado → lâmpada LIGADA
    // HIGH → relé aberto  → lâmpada DESLIGADA
  }
}
