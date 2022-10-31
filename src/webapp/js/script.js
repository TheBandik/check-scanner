function setThemeClass() {
    document.documentElement.className = Telegram.WebApp.colorScheme;
}
Telegram.WebApp.onEvent('themeChanged', setThemeClass);
setThemeClass();

Telegram.WebApp.ready();

const initData = Telegram.WebApp.initData || '';
const initDataUnsafe = Telegram.WebApp.initDataUnsafe || {};
webviewExpand();
document.querySelector('#greeting').innerHTML = `Hi, ${initDataUnsafe.user.first_name}!`;
document.querySelector('#initData').innerHTML = JSON.stringify(initData, null, 2);
document.querySelector('#initDataUnsafe').innerHTML = JSON.stringify(initDataUnsafe, null, 2);
document.querySelector('#themeData').html(JSON.stringify(Telegram.WebApp.themeParams, null, 2));
Telegram.WebApp.MainButton
    .setText('CLOSE WEBVIEW')
    .show()
    .onClick(function () { webviewClose(); });
Telegram.WebApp.onEvent('themeChanged', function () {
    document.querySelector('#themeData').innerHTML = JSON.stringify(Telegram.WebApp.themeParams, null, 2);
});
function toggleMainButton(el) {
    const mainButton = Telegram.WebApp.MainButton;
    if (mainButton.isVisible) {
        mainButton.hide();
        el.innerHTML = 'Show Main Button';
    } else {
        mainButton.show();
        el.innerHTML = 'Hide Main Button';
    }
}
function webviewExpand() {
    Telegram.WebApp.expand();
}
function webviewClose() {
    Telegram.WebApp.close();
}
function sendTime(spam) {
    const repeat = spam ? 10 : 1;
    for (let i = 0; i < repeat; i++) {
        Telegram.WebApp.sendData(new Date().toString());
    }
}
function test() {
    Telegram.WebApp.sendData("test");
}
function requestLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            document.querySelector('#locationData').innerHTML = '(' + position.coords.latitude + ', ' + position.coords.longitude + ')';
        });
    } else {
        document.querySelector('#locationData').innerHTML = '(Geolocation is not supported in this browser)';
    }
    return false;
}
function requestVideo() {
    if (navigator.mediaDevices) {
        navigator.mediaDevices.getUserMedia({ audio: false, video: true }).then(function (stream) {
            document.querySelector('#videoData').innerHTML = '(Access granted)';
        });
    } else {
        document.querySelector('#videoData').innerHTML = '(Media devices is not supported in this browser)';
    }
    return false;
}
function requestAudio() {
    if (navigator.mediaDevices) {
        navigator.mediaDevices.getUserMedia({ audio: true, video: false }).then(function (stream) {
            document.querySelector('#audioData').innerHTML = '(Access granted)';
        });
    } else {
        document.querySelector('#audioData').innerHTML = '(Media devices is not supported in this browser)';
    }
    return false;
}