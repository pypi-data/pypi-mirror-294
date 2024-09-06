def validar_ambiente(input_text):
    # Validar el texto de entrada
    if input_text is None or input_text.strip() == "" or input_text.lower() != "prod":
        ambiente_input = "dev"
    else:
        ambiente_input = "prod"
    return ambiente_input