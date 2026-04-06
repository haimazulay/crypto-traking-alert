import pytest
from unittest.mock import patch, mock_open
from src.notifier import EmailNotifier

def test_notifier_init():
    notifier = EmailNotifier("a@b.com", "pass", "c@d.com")
    assert notifier.sender_email == "a@b.com"
    assert notifier.receiver_email == "c@d.com"

@patch("src.notifier.smtplib.SMTP_SSL")
@patch("os.path.exists", return_value=True)
def test_notifier_send_email_with_graph(mock_exists, mock_smtp):
    notifier = EmailNotifier("a@b.com", "pass", "c@d.com")
    m_open = mock_open(read_data=b"imagedata")
    
    with patch("builtins.open", m_open):
        notifier.send_email(50000.0, "fake.png")
    
    # Assert SMTP logic
    mock_smtp.assert_called_once()
    mock_instance = mock_smtp.return_value.__enter__.return_value
    mock_instance.login.assert_called_with("a@b.com", "pass")
    mock_instance.send_message.assert_called_once()

@patch("src.notifier.smtplib.SMTP_SSL")
@patch("os.path.exists", return_value=False)
def test_notifier_send_email_no_graph(mock_exists, mock_smtp):
    notifier = EmailNotifier("a@b.com", "pass", "c@d.com")
    notifier.send_email(50000.0, "fake.png")
    
    mock_smtp.assert_called_once()
    mock_instance = mock_smtp.return_value.__enter__.return_value
    mock_instance.send_message.assert_called_once()

@patch("src.notifier.smtplib.SMTP_SSL")
@patch("os.path.exists", return_value=False)
def test_notifier_send_email_exception(mock_exists, mock_smtp, capsys):
    notifier = EmailNotifier("a@b.com", "pass", "c@d.com")
    mock_smtp.side_effect = Exception("SMTP Error Connection Refused")
    
    notifier.send_email(50000.0, "fake.png")
    
    captured = capsys.readouterr()
    assert "Failed to send email: SMTP Error Connection Refused" in captured.out
