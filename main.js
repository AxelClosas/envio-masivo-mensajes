const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const fs = require('fs');
const qrcode = require('qrcode-terminal');
// import path from 'path'
const path = require('path')

// Inicializar el cliente de WhatsApp Web
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: { headless: true }
});

// Cargar la lista de contactos
const contactsFile = 'contacts.json';
const logFile = 'log.json';

// Leer contactos desde el archivo JSON
const readContacts = () => {
    try {
        return JSON.parse(fs.readFileSync(contactsFile, 'utf8'));
    } catch (error) {
        console.error("Error leyendo el archivo de contactos:", error);
        return [];
    }
};

// Guardar log de mensajes enviados
const saveLog = (number, status) => {
    let logs = [];
    try {
        logs = JSON.parse(fs.readFileSync(logFile, 'utf8'));
    } catch (error) {
        // Si el archivo no existe, se crea con un array vacío
    }

    logs.push({ number, status, timestamp: new Date().toISOString() });

    fs.writeFileSync(logFile, JSON.stringify(logs, null, 2));
};

// Cuando se genere el QR para iniciar sesión
client.on('qr', qr => {
    console.log("Escanea el siguiente código QR para iniciar sesión:");
    qrcode.generate(qr, { small: true });
});

// Cuando el cliente esté listo
client.on('ready', async () => {
    console.log("Cliente de WhatsApp listo.");

    // Path PDF
    const pdfPath = path.join(__dirname, '🛡️ Guía de Primer Acceso a HIS mediante Identity Server.pdf')
    
    // Cargar el archivo como base64
    const pdfData = fs.readFileSync(pdfPath).toString('base64')

    // Crear objeto MessageMedia
    const media = new MessageMedia('application/pdf', pdfData, '🛡️ Guía de Primer Acceso a HIS mediante Identity Server.pdf')

    const contacts = readContacts();
    
    for (const contact of contacts) {
        const number = contact.number;
        const message = contact.message;
        const formattedNumber = number.includes('@c.us') ? number : `${number}@c.us`;

        try {
            const isRegistered = await client.isRegisteredUser(formattedNumber);

            if (!isRegistered) {
                console.log(`❌ Número no registrado en WhatsApp: ${number}`);
                saveLog(number, 'No registrado');
                continue;
            }

            await client.sendMessage(formattedNumber, media, {caption: message});
            console.log(`✅ Mensaje enviado a: ${number}`);
            saveLog(number, 'Enviado');
        } catch (error) {
            console.error(`⚠️ Error enviando a ${number}:`, error);
            saveLog(number, 'Error');
        }
    }

    console.log("📩 Mensajes enviados.");
});

// Manejo de errores
client.on('auth_failure', msg => {
    console.error("❌ Fallo de autenticación", msg);
});

client.initialize();
