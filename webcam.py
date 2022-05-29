from flask import Flask, render_template_string, request


app = Flask('app')

@app.route('/')
def index():
    return render_template_string('''
    <video id="player" controls autoplay></video>
<script>
  const player = document.getElementById('player');

  const constraints = {
    video: true,
  };

  navigator.mediaDevices.getUserMedia(constraints).then((stream) => {
    player.srcObject = stream;
  });
</script>''')

app.run('0.0.0.0', port=3000)
