# User-Driven File Compression System

This project provides a graphical user interface (GUI) for compressing and decompressing files using various algorithms. It supports multiple file formats including text, PDF, documents, and images with intelligent algorithm selection based on file type and compression level.

## Features

- **Multiple Compression Algorithms:**
  - LZW (for text files - high compression)
  - Huffman coding (for text files - low compression)
  - RLE (for text files - optimal compression)
  - LZMA (for PDF/DOC - high compression)
  - BZIP2 (for PDF/DOC - optimal compression)
  - ZIP (for images and general files)
  - Special handling for BMP images with lossy/lossless options

- **User-Friendly Interface:**
  - Drag-and-drop file support
  - Compression size estimates
  - Progress indicators
  - Modern UI design

## Project Structure

```
User-Driven-File-Compression-System
├── Algorithms/
│   ├── huffman.py    # Huffman compression
│   ├── lzw.py        # LZW compression
│   ├── rle.py        # Run-Length Encoding
│   ├── bz2_algo.py   # BZIP2 compression
│   ├── lzma_algo.py  # LZMA compression
│   └── zip_algo.py   # ZIP compression
├── main.py           # Main GUI application
└── README.md         # Documentation
```

## Getting Started

1. **Prerequisites:**
   ```
   Python 3.x
   tkinterdnd2
   Pillow (for image handling)
   ```

2. **Installation:**
   ```
   git clone <repository-url>
   cd User-Driven-File-Compression-System
   pip install tkinterdnd2 Pillow
   ```

3. **Run the application:**
   ```
   python main.py
   ```

## Usage

1. **Compression:**
   - Select or drag-and-drop a file
   - Choose compression level (High/Low/Optimal)
   - For BMP files, choose between lossy or lossless compression
   - Click "Compress File" and select output location

2. **Decompression:**
   - Click "Decompress File"
   - Select a compressed file (.lzw, .huff, .rle, .zip, .bz2, .xz)
   - Choose output location
   - For ZIP files, select extraction directory

## Supported File Types

- **Text Files (.txt)**
  - High: LZW compression
  - Low: Huffman coding
  - Optimal: RLE

- **Documents (.pdf, .doc, .docx)**
  - High: LZMA compression
  - Low: ZIP compression
  - Optimal: BZIP2 compression

- **Images (.jpg, .jpeg, .png)**
  - ZIP compression

- **BMP Images**
  - Lossless: PNG conversion
  - Lossy: JPEG conversion

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.