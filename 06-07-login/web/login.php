<!DOCTYPE html>
<html>

<head>
  <link rel="stylesheet" type="text/css" href="style.css" />
</head>

<body>

<?php

// echo 'get: ' . json_encode($_GET) . '<br>';
// echo 'post: ' . json_encode($_POST) . '<br>';

// after the page reloads, print them out
if (isset($_POST['name'])){
    if ( ( $_POST['name'] == 'caca' ||  $_POST['name'] == 'hadoop' ) && $_POST['password'] == 'c'){
        if (session_status() == PHP_SESSION_NONE) {
            session_start();
        }
        $session_id = md5(date("D M j G:i:s T Y") + rand());
        $_SESSION[$_POST['name']] = $session_id;
        $_SESSION['user'] = $_POST['name'];
        
        // set the cookies
        setcookie("session[name]", $_POST['name']);
        setcookie("session[id]", $session_id, time()+3600);  /* expire in 1 hour */
        setcookie("session[logintime]", date("D M j G:i:s T Y"), time()+3600);  /* expire in 1 hour */
        setcookie("session[subid]", "28727283829", time()+3600, "/sub/", "jc.lo"); /* only accessiable to /sub/ dir and jc.lo domain*/
        
        header('Location: main.php', true, 302);
    } else {
        if ( isset($_POST['name']) && isset($_POST['password']))
            echo '<script type="text/javascript">alert("用户名或密码错误");</script>';
    }
}

?>

  <div class='login-input-block'>

    <img src="chlogo.png" alt="">

    <form action="login.php" method="POST">
      <div class='input-box'>
        <!--<div style="width: 100px;display: inline-block;">Name:</div> -->
        <input class='input-field' type="text" name="name" placeholder="User Name">
      </div>
      <div class='input-box'>
        <!-- <div style="width: 100px; display: inline-block;">Password</div> -->
        <input class='input-field' type="password" name="password" placeholder="Password">
      </div>
      <div class="ed-login">
        <input type="submit" value="Login">
      </div>
    </form>
  </div>

</body>

</html>