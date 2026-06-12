from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


OWNER_ID = 7396716019


from datetime import datetime


async def cek_user(update, context):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("Bot ini khusus pemilik.")
        return False
    return True

saldo = 0
riwayat = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bot Keuangan Aktif!\n\n"
        "/masuk jumlah keterangan\n"
        "/keluar jumlah keterangan\n"
        "/saldo sisa saldo\n"
        "/riwayat pengeluarannya\n"
        "/menabung jumlah masukan tabungan\n"
        "/tabungan total tabungan\n"
   )

async def masuk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global saldo
    try:
        jumlah = int(context.args[0])
        ket = " ".join(context.args[1:])
        saldo += jumlah
        riwayat.append(f"+ Rp{jumlah:,} {ket}")

        await update.message.reply_text(
            f"✅ Pemasukan ditambahkan\n"
            f"Rp{jumlah:,} - {ket}\n\n"
            f"Saldo sekarang: Rp{saldo:,}"
        )
    except:
        await update.message.reply_text("Contoh: /masuk 150000 uang jajan")

async def keluar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global saldo
    try:
        jumlah = int(context.args[0])
        ket = " ".join(context.args[1:])
        saldo -= jumlah
        riwayat.append(f"- Rp{jumlah:,} {ket}")

        await update.message.reply_text(
            f"❌ Pengeluaran ditambahkan\n"
            f"Rp{jumlah:,} - {ket}\n\n"
            f"Saldo sekarang: Rp{saldo:,}"
        )
    except:
        await update.message.reply_text("Contoh: /keluar 25000 beli makan")

async def cek_saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"💰 Saldo saat ini: Rp{saldo:,}")

async def lihat_riwayat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not riwayat:
        await update.message.reply_text("Belum ada transaksi.")
        return

    teks = "📋 Riwayat Transaksi\n\n" + "\n".join(riwayat)
    await update.message.reply_text(teks)



async def pengeluaran(update, context):
    global saldo

    jumlah = int(context.args[0])

    if jumlah > saldo:
        await update.message.reply_text("❌ Saldo tidak cukup!")
        return

    saldo -= jumlah

    await update.message.reply_text(
        f"💸 Pengeluaran Rp{jumlah:,}\n"
        f"💰 Sisa saldo: Rp{saldo:,}"
    )






TOKEN = "8668164154:AAHVHx10bi4_lorPQSUAC6WGCxD_1IlAHBs"

tabungan = {}

async def menabung(update, context):
    user_id = update.effective_user.id

    if len(context.args) != 1:
        await update.message.reply_text("Gunakan: /menabung jumlah")
        return

    jumlah = int(context.args[0])

    if user_id not in tabungan:
        tabungan[user_id] = 0

    tabungan[user_id] += jumlah

    await update.message.reply_text(
        f"💰 Berhasil menabung Rp{jumlah:,}\n"
        f"Total tabungan: Rp{tabungan[user_id]:,}"
    )

async def lihat_tabungan(update, context):
    user_id = update.effective_user.id

    total = tabungan.get(user_id, 0)

    await update.message.reply_text(
        f"💰 Total tabungan kamu: Rp{total:,}"    )



waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


async def notifikasi(update, jenis, jumlah, saldo, tabungan, total_pemasukan, total_pengeluaran):
    await update.message.reply_text(
        f"📢 TRANSAKSI BERHASIL\n\n"
        f"📝 Jenis: {jenis}\n"
        f"💵 Jumlah: Rp{jumlah:,}\n\n"
        f"📊 RINGKASAN KEUANGAN\n"
        f"💰 Saldo: Rp{saldo:,}\n"
        f"🏦 Tabungan: Rp{tabungan:,}\n"
        f"📈 Total Pemasukan: Rp{total_pemasukan:,}\n"
        f"📉 Total Pengeluaran: Rp{total_pengeluaran:,}"
    )





app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("masuk", masuk))
app.add_handler(CommandHandler("keluar", keluar))
app.add_handler(CommandHandler("saldo", cek_saldo))
app.add_handler(CommandHandler("riwayat", lihat_riwayat))
app.add_handler(CommandHandler("menabung", menabung))
app.add_handler(CommandHandler("tabungan", lihat_tabungan))

print("Bot aktif...")
app.run_polling()
