function binaryToText(binaryStr) {
    let text = "";
    for (let i = 0; i < binaryStr.length; i += 8) {
        const byte = binaryStr.slice(i, i + 8);
        text += String.fromCharCode(parseInt(byte, 2));
    }
    return text;
}

function decryptBinary(encryptedBinary, key) {
    const [k1, k2, k3, k4] = key.map(Number); // ensure key values are numbers
    let decrypted = "";

    for (let i = 0; i < encryptedBinary.length; i += 8) {
        let byte = encryptedBinary.slice(i, i + 8);
        if (byte.length < 8) {
            byte = byte.padEnd(8, '0');
        }
        let b = parseInt(byte, 2);

        b = ((b << k4) | (b >>> (8 - k4))) & 0xFF; // left rotate
        b ^= k3;
        b = ((b >>> k2) | (b << (8 - k2))) & 0xFF; // right rotate
        b ^= k1;

        decrypted += b.toString(2).padStart(8, '0');
    }

    return binaryToText(decrypted);
}

function decryptFromPage(keyInputId, encryptedContainerId) {
    const keyInput = document.getElementById(keyInputId)?.value.trim();
    const encryptedElem = document.getElementById(encryptedContainerId);

    if (!keyInput || !encryptedElem) {
        alert("missing key or encrypted text");
        return;
    }
    const encryptedText = encryptedElem.textContent.trim();
    
    if (keyInput.length !== 4 || /\D/.test(keyInput)) {
        alert("please enter a valid 4-digit numeric key");
        return;
    }
    const keyParts = keyInput.split("").map(d => parseInt(d));

    try {
        const decryptedText = decryptBinary(encryptedText, keyParts);
        encryptedElem.textContent = decryptedText;
    } catch (err) {
        alert("decryption error");
    }
}