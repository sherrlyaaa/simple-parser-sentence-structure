class StateFAMachine:
    def __init__(self, state):
        # Menginisialisasi dengan daftar status dan status awal
        self.state = state
        self.currentState = 0

    def reset(self):
        # Mengatur ulang status ke awal
        self.currentState = 0

    def processChar(self, char):
        # Memproses setiap karakter dalam kata
        possible_next_state = []
        for state in self.state:
            # Memeriksa apakah karakter saat ini cocok dengan karakter pada posisi saat ini dalam salah satu status yang valid
            if len(state) > self.currentState and state[self.currentState] == char:
                possible_next_state.append(state)
        
        if not possible_next_state:
            # Jika tidak ada status yang cocok, kembalikan False
            return False

        # Memperbarui daftar status yang valid dan menaikkan status saat ini
        self.state = possible_next_state
        self.currentState += 1
        return True

    def isAccepted(self):
        # Memeriksa apakah kata yang sedang diproses cocok dengan salah satu status yang valid
        return any(len(state) == self.currentState for state in self.state)

def tokenize(sentence):
    # Definisi set untuk masing-masing kategori kata
    subjek = {'pelajar', 'seniman', 'atlet', 'penulis', 'petani'}
    predikat = {'mempelajari', 'menulis', 'melukis', 'berlari', 'menanam'}
    objek = {'teori', 'potret', 'maraton', 'novel', 'padi'}
    keterangan = {'seksama', 'indah', 'cepat', 'semangat', 'sabar'}

    # Gabungkan semua kategori dalam satu set untuk pengecekan
    all_words = subjek | predikat | objek | keterangan

    # Memisahkan kalimat menjadi token
    tokens = sentence.split()
    recognizedTokens = []

    # Mengenali setiap token
    for token in tokens:
        sm = StateFAMachine(all_words)  # Membuat instansi StateMachine baru untuk setiap token
        for char in token:
            if not sm.processChar(char):
                return False, []  # Token tidak dikenali, kembalikan False dan daftar kosong

        if sm.isAccepted():
            # Menambahkan jenis token yang dikenali ke daftar recognized_tokens
            if token in subjek:
                recognizedTokens.append('S')  # Tambahkan 'S' jika token adalah subjek
            elif token in predikat:
                recognizedTokens.append('P')  # Tambahkan 'P' jika token adalah predikat
            elif token in objek:
                recognizedTokens.append('O')  # Tambahkan 'O' jika token adalah objek
            elif token in keterangan:
                recognizedTokens.append('K')  # Tambahkan 'K' jika token adalah keterangan
        else:
            return False, []  # Token tidak dikenali, kembalikan False dan daftar kosong

    return True, recognizedTokens  # Kembalikan True dan daftar recognized_tokens

def parse_sentence(sentence):
    # Memanggil fungsi tokenize untuk mengenali token
    isValid, token = tokenize(sentence)
    if not isValid:
        return False, []  # Jika kalimat tidak valid, kembalikan False dan daftar kosong

    # Definisikan struktur kalimat yang valid
    validStructures = [
        ['S', 'P', 'O', 'K'],  # Struktur S-P-O-K
        ['S', 'P', 'K'],       # Struktur S-P-K
        ['S', 'P', 'O'],       # Struktur S-P-O
        ['S', 'P']             # Struktur S-P
    ]

    # Memeriksa apakah urutan token sesuai dengan salah satu struktur yang valid
    if token in validStructures:
        return True, token  # Jika sesuai, kembalikan True dan urutan token
    else:
        return False, token  # Jika tidak sesuai, kembalikan False dan urutan token

def main():
    while True:
        # Menerima input kalimat dari pengguna
        sentence = input("Masukkan kalimat (atau ketik 'keluar' untuk berhenti): ")
        
        # Keluar dari loop jika pengguna mengetik 'keluar'
        if sentence.lower() == 'keluar':
            break
        
        # Memeriksa validitas kalimat menggunakan parse_sentence
        isValid, token = parse_sentence(sentence)
        
        # Menampilkan hasil pemeriksaan
        if isValid:
            print(f"Kalimat valid: {sentence}")
            print(f"Struktur token: {token}")
        else:
            print(f"Kalimat tidak valid: {sentence}")
            print(f"Struktur token: {token}")

# Menjalankan fungsi utama
if __name__ == "__main__":
    main()
