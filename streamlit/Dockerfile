# Usa una imagen base de Python
FROM python:3.9

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios
COPY requirements.txt .
COPY app.py .
COPY data /app/data
COPY pages /app/pages

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 8501
EXPOSE 8501

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "app.py"]