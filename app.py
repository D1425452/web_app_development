from app import create_app

app = create_app()

if __name__ == '__main__':
    # 開發模式下啟動伺服器
    app.run(debug=True)
