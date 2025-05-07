import webbrowser

def run(assistant):
    try:
        webbrowser.open("https://mail.google.com")
        print("✅ Gmail opened successfully!")
    except Exception as e:
        print(f"❌ Failed to open Gmail: {e}")
        # written by @GWSURYA