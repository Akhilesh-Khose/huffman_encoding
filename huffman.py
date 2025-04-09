import heapq
from collections import Counter
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Huffman Node
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

# Build Huffman Tree
def build_huffman_tree(text):
    freq = Counter(text)
    heap = [Node(ch, fr) for ch, fr in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        merged = Node(None, n1.freq + n2.freq)
        merged.left = n1
        merged.right = n2
        heapq.heappush(heap, merged)

    return heap[0]

# Generate codes
def generate_codes(root, current_code="", codes={}):
    if root is None:
        return

    if root.char is not None:
        codes[root.char] = current_code
        return

    generate_codes(root.left, current_code + "0", codes)
    generate_codes(root.right, current_code + "1", codes)
    return codes

# Encode
def encode_text(text, codes):
    return ''.join(codes[ch] for ch in text)

# Decode
def decode_text(encoded, root):
    decoded = ''
    node = root
    for bit in encoded:
        node = node.left if bit == '0' else node.right
        if node.char:
            decoded += node.char
            node = root
    return decoded

# --- GUI Starts Here ---

def run_huffman():
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Warning", "Please enter some text.")
        return

    root = build_huffman_tree(text)
    codes = generate_codes(root)

    encoded = encode_text(text, codes)
    decoded = decode_text(encoded, root)

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"Character Codes:\n")
    for ch in codes:
        output_text.insert(tk.END, f"'{ch}': {codes[ch]}\n")

    output_text.insert(tk.END, f"\nEncoded Text:\n{encoded}\n")
    output_text.insert(tk.END, f"\nDecoded Text:\n{decoded}\n")
    output_text.insert(tk.END, f"\nOriginal Bits: {len(text) * 8}\nEncoded Bits: {len(encoded)}\n")

# GUI Layout
window = tk.Tk()
window.title("Huffman Encoder/Decoder")
window.geometry("700x600")
window.resizable(False, False)

tk.Label(window, text="Enter Text to Encode:", font=("Arial", 12)).pack(pady=5)
input_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=6, font=("Courier", 10))
input_text.pack()

tk.Button(window, text="Run Huffman Encoding", font=("Arial", 12), command=run_huffman).pack(pady=10)

tk.Label(window, text="Output:", font=("Arial", 12)).pack(pady=5)
output_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=20, font=("Courier", 10))
output_text.pack()

window.mainloop()
