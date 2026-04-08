const axios = require("axios");
const qrcode = require("qrcode-terminal");
const { Client, LocalAuth } = require("whatsapp-web.js");

const WEBHOOK_URL = "http://backend:8000/api/v1/ai-assistant/whatsapp/webhook/";

const client = new Client({
  authStrategy: new LocalAuth({
    dataPath: ".wwebjs_auth",
  }),
  puppeteer: {
    executablePath: "/usr/bin/chromium-browser",
    args: [
      "--no-sandbox",
      "--disable-setuid-sandbox",
      "--disable-dev-shm-usage",
    ],
  },
});

client.on("qr", (qr) => {
  console.log("Scan this QR code with WhatsApp:");
  qrcode.generate(qr, { small: true });
});

client.on("ready", () => {
  console.log("WhatsApp bridge is ready.");
});

client.on("message", async (msg) => {
  const messageBody = (msg.body || "").trim();
  if (!messageBody) {
    return;
  }

  try {
    const { data } = await axios.post(WEBHOOK_URL, {
      phone: msg.from,
      message: messageBody,
    }, {
      headers: {
        "Content-Type": "application/json",
        "Idempotency-Key": `wa-${Date.now()}-${Math.random()}`,
      },
    });

    let reply = data.response || "No response generated.";
    if (data.intent) {
      reply += `\n\nIntent: ${data.intent}`;
    }
    if (data.quotation_id) {
      reply += `\nQuotation ID: ${data.quotation_id}`;
    }

    await client.sendMessage(msg.from, reply);
  } catch (error) {
    const detail =
      error.response?.data?.detail ||
      error.response?.data?.error?.message ||
      error.message;
    await client.sendMessage(
      msg.from,
      `Theoinc assistant is temporarily unavailable.\n${detail}`
    );
  }
});

client.initialize();
