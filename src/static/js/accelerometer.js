export function getAccelerometer() {
    console.log("hii accelerometer")
  return new Promise((resolve, reject) => {
    if (window.DeviceMotionEvent) {
      window.addEventListener('devicemotion', (event) => {
        const { x, y, z } = event.accelerationIncludingGravity;
        resolve({ x, y, z });
      });
    } else {
      reject('DeviceMotionEvent is not supported');
    }
  });
}

export function getOrientation() {
    return new Promise((resolve, reject) => {
        if (window.DeviceOrientationEvent) {
        window.addEventListener('deviceorientation', (event) => {
            const { alpha, beta, gamma } = event;
            resolve({ alpha, beta, gamma });
        });
        } else {
        reject('DeviceOrientationEvent is not supported');
        }
    });
}

// Path: static/js/gyroscope.js
export function getGyroscope() {
    return new Promise((resolve, reject) => {
        if (window.DeviceMotionEvent) {
        window.addEventListener('devicemotion', (event) => {
            const { x, y, z } = event.rotationRate;
            resolve({ x, y, z });
        });
        } else {
        reject('DeviceMotionEvent is not supported');
        }
    });
}

// Path: static/js/magnetometer.js
export function getMagnetometer() {
    return new Promise((resolve, reject) => {
        if (window.DeviceMotionEvent) {
        window.addEventListener('devicemotion', (event) => {
            const { x, y, z } = event.rotationRate;
            resolve({ x, y, z });
        });
        } else {
        reject('DeviceMotionEvent is not supported');
        }
    });
}

// Path: static/js/compass.js
export function getCompass() {
    return new Promise((resolve, reject) => {
        if (window.DeviceOrientationEvent) {
        window.addEventListener('deviceorientation', (event) => {
            const { alpha, beta, gamma } = event;
            resolve({ alpha, beta, gamma });
        });
        } else {
        reject('DeviceOrientationEvent is not supported');
        }
    });
}

// Path: static/js/location.js
export function getLocation() {
    return new Promise((resolve, reject) => {
        if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
            const { latitude, longitude } = position.coords;
            resolve({ latitude, longitude });
        });
        } else {
        reject('Geolocation is not supported');
        }
    });
}


