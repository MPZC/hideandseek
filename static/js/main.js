const modeSwitch = document.getElementById('modeSwitch');
const modeLabel = document.getElementById('modeLabel');
const encodeSection = document.getElementById('encode-section');
const decodeSection = document.getElementById('decode-section');

modeSwitch.addEventListener('change', () => {
    if (modeSwitch.checked) {
        encodeSection.classList.remove('active');
        decodeSection.classList.add('active');
        modeLabel.textContent = 'Mode: Decode';
    } else {
        decodeSection.classList.remove('active');
        encodeSection.classList.add('active');
        modeLabel.textContent = 'Mode: Encode';
    }
});
