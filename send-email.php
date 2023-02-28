<?php
if(isset($_POST['name']) && isset($_POST['email']) && isset($_POST['message'])) {
    $name = $_POST['name'];
    $email = $_POST['email'];
    $message = $_POST['message'];
    $to = 'hanlbomi@gmail.com'; // Your email address here
    $subject = 'New message from your website';
    $body = "Name: $name\nEmail: $email\n\n$message";
    $headers = "From: $email";

    if(mail($to, $subject, $body, $headers)) {
        echo 'Message sent successfully.';
    } else {
        echo 'An error occurred. Please try again later.';
    }
}
?>
