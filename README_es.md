# Paper Reader

Herramienta en Python que resume automáticamente papers académicos en PDF usando Google Gemini AI y genera resúmenes estructurados en formato LaTeX, listos para usar con `\input{}` en Overleaf.

## Qué hace

- Lee PDFs desde `papers/input/tu-carpeta/`
- Aplica un template personalizable para estructurar el resumen
- Genera un archivo `.tex` por cada paper
- Guarda los outputs en `papers/output/tu-carpeta/`
- Omite papers ya procesados (sesiones reanudables)
- Procesa hasta 15 papers por sesión con pausas automáticas

## Templates

Se incluyen dos templates:

- **default** — para papers de economía general: pregunta de investigación, marco teórico, estrategia empírica, datos, hallazgos, mecanismos, supuestos, limitaciones, contribución, extensiones. Prompt escrito en español.
- **default_en** — misma estructura, prompt escrito en inglés.

Puedes crear tu propio template agregando un archivo `.txt` a la carpeta `templates/`. No se requiere ningún formato especial — solo escribe en texto plano las instrucciones que quieres que siga el modelo.

## Requisitos

- Python 3.8+
- API key de Google Gemini (tier gratuito disponible en [aistudio.google.com](https://aistudio.google.com))

## Instalación

1. Clona el repositorio
   ```
   git clone https://github.com/vladimir-banos/paper-reader.git
   cd paper-reader
   ```

2. Instala las dependencias
   ```
   pip install -r requirements.txt
   ```

3. Crea un archivo `.env` en la carpeta raíz
   ```
   GEMINI_API_KEY=tu_api_key_aqui
   ```

4. Coloca tus PDFs en `papers/input/nombre-de-carpeta/`

## Uso

```
python main.py
```

El programa te pedirá seleccionar un template y una carpeta. Los resúmenes se guardan como archivos `.tex` en `papers/output/`.

## Estructura del proyecto

```
paper-reader/
├── main.py
├── config.py
├── requirements.txt
├── .env              ← tu API key (no se sube a GitHub)
├── .gitignore
├── templates/
│   ├── default.txt
│   └── default_en.txt
└── papers/
    ├── input/        ← coloca tus PDFs aquí
    └── output/       ← resúmenes generados aquí
```

## Autor

Vladimir Baños — Estudiante de Economía, Universidad de Piura (UDEP)  
Intereses de investigación: microeconomía aplicada, organización industrial, economía del desarrollo

---

*README also available in [English](README.md)*