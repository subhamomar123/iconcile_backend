from flask import Blueprint, send_from_directory

bp = Blueprint("swagger_routes", __name__)


@bp.route("/swagger/<path:filename>")
def swagger_static(filename):
    return send_from_directory("swagger", filename)


@bp.route("/swagger/")
def swagger_ui():
    return """
    <html>
        <head>
            <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.0.0/swagger-ui.css">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.0.0/swagger-ui-bundle.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.0.0/swagger-ui-standalone-preset.js"></script>
        </head>
        <body>
            <div id="swagger-ui"></div>
            <script>
                const ui = SwaggerUIBundle({
                    url: "/swagger/swagger.json",
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIStandalonePreset
                    ],
                    layout: "StandaloneLayout"
                });
            </script>
        </body>
    </html>
    """
