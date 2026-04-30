# Sistema de Controle Térmico via PWM Simulado

Projeto desenvolvido para a disciplina de Sistemas Dinâmicos e Controle (FIAP), focado na implementação de um sistema de malha aberta para controle de temperatura em ambiente fechado. O sistema utiliza a técnica de modulação por largura de pulso (PWM) simulada via software para gerenciar a potência de uma carga resistiva AC através de um microcontrolador.

---

## Arquitetura do Sistema

O projeto é dividido em três camadas principais:

- **Hardware e Atuação:** Controle de carga AC (Lâmpada Incandescente 15W) via Módulo Relé e monitoramento térmico via sensor analógico LM35.
- **Firmware (Arduino):** Implementação de lógica não-bloqueante para processamento de sinais serial e gerenciamento de ciclos PWM com período fixo de 30 segundos.
- **Interface de Telemetria (Python):** Dashboard para visualização de dados em tempo real, operando com frequência de amostragem de 1Hz.

---

## Funcionalidades Técnicas

- Gerenciamento PWM: Ciclos configuráveis de 30 segundos para controle de potência AC.
- Protocolo de Comunicação: Interface Serial a 9600 bps com processamento de strings não-bloqueante.
- Monitoramento em Tempo Real: Gráfico dinâmico com janela deslizante para análise de inércia térmica.
- Cálculo de Duty Cycle: Demonstração visual instantânea dos tempos de condução (T_on) e corte (T_off).

---

## Especificações de Hardware

- Microcontrolador: Arduino Uno R3.
- Sensor de Temperatura: LM35 (Escala de 10mV/°C).
- Atuador: Módulo Relé 5V (Active Low).
- Carga: Lâmpada Incandescente 15W (Base E27).
- Ambiente: Câmara de madeira isolada (30x30x20cm).

---

## Stack Tecnológica

- Linguagem C++: Firmware otimizado com a função `millis()` para evitar travamentos de loop.
- Python 3.12+: Backend para processamento de telemetria e comunicação via pyserial.
- Streamlit: Framework para interface de usuário e plotagem de dados.
- Pandas: Estruturação de buffers de dados para visualização temporal.

---

## Estrutura do Repositório

```plaintext
├── arduino/
│   └── controle_termico.ino  # Código fonte do microcontrolador
├── python/
│   └── app.py                # Interface de telemetria e controle
└── README.md                 # Documentação técnica
````
