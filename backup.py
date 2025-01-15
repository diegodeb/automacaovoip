from flask import Flask, render_template, request
import html

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    generated_text = None  # Variável para armazenar o texto gerado
    if request.method == 'POST':
        mac = request.form['mac']
        username = request.form['username']
        ippabx = request.form['ippabx']
        label = request.form['label']
        password = request.form['password']

        # Conteúdo do texto formatado com as variáveis preenchidas
        generated_text = f"""
MAC: {mac}
USERNAME: {username}
IPPABX: {ippabx}
LABEL: {label}
PASSWORD: {password}

let serial=declare("Device.DeviceInfo.SerialNumber",{{value:1}}).value[0];
/*{mac}*/ 
if("{mac}"==serial){{
    declare("Device.Services.VoiceService.1.VoiceProfile.1.Line.1.Enable", null, {{value:"Enabled"}});
    declare("Device.Time.NTPServer1", null, {{value:"ntp.ufrn.br"}});
    declare("Device.UserInterface.X_001565_Language.X_001565_GUILanguage", null, {{value:"Portuguese"}});
    declare("Device.UserInterface.X_001565_Language.X_001565_WebLanguage", null, {{value:"Portuguese"}});
    declare("Device.UserInterface.X_001565_Update.X_001565_AdminPassword", null, {{value:"qmnases"}});
    declare("Device.Services.VoiceService.1.VoiceProfile.1.Line.1.SIP.AuthUserName", 1, {{value: "{username}"}});
    declare("Device.Services.VoiceService.1.VoiceProfile.1.Line.1.SIP.X_001565_UserName", null, {{value: "{username}"}});
    declare("Device.Services.VoiceService.1.VoiceProfile.1.SIP.UserAgentDomain", 1, {{value: "{ippabx}"}});
    declare("Device.Services.VoiceService.1.VoiceProfile.1.SIP.RegistrarServer", null, {{value: "{ippabx}"}});
    declare("Device.Services.VoiceService.1.VoiceProfile.1.SipServer.1.RegistrarServer", null, {{value: "{ippabx}"}});
    declare("Device.Services.VoiceService.1.VoiceProfile.1.Line.1.SIP.URI", null, {{value:"sip:"+"{username}"+"@"+"{ippabx}"}});
    declare("Device.Services.VoiceService.1.VoiceProfile.1.Line.1.SIP.X_001565_Label", null, {{value:"{label}"}});
    declare("Device.Services.VoiceService.1.VoiceProfile.1.Line.1.CallingFeatures.CallerIDName", null, {{value:"{label}"}});
    declare("Device.Services.VoiceService.1.VoiceProfile.1.Line.1.SIP.X_001565_DisplayName", null, {{value:"{label}"}});
    declare("Device.Services.VoiceService.1.VoiceProfile.1.Line.1.SIP.AuthPassword", 1, {{value:"{password}"}});
}}
"""

    return render_template('form.html', generated_text=generated_text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)

