from flask import Flask, render_template_string, request


app = Flask('app')

@app.route('/')
def index():
    return render_template_string('''
    <video id="player" controls autoplay></video>
    <script>
        var player = document.getElementById('player');

        const constraints = {
            video: true,
        };

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        player.srcObject = stream;
        player.play();
    });
    }
    </script>''')

app.run('0.0.0.0', port=3000)
