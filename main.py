from app import create_app   # Importa la función create_app que inicializa la app Flask con configuraciones y rutas

app = create_app()     # Crea la instancia de la aplicación Flask usando el patrón de aplicación factoría

if __name__ == "__main__":    # Verifica si el archivo se está ejecutando directamente (no importado como módulo)
    app.run(debug=True)       # Ejecuta el servidor de desarrollo en modo debug (recarga automática y errores detallados)

