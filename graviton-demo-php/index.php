<!DOCTYPE html>
<html lang="en">

    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>Simple PHP App</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="assets/css/bootstrap.min.css" rel="stylesheet">
        <style>body {margin-top: 40px; background-color: #333; background-image: url('assets/img/wallhaven-76r359.jpg')}</style>
        <link href="assets/css/bootstrap-responsive.min.css" rel="stylesheet">
        <!--[if lt IE 9]><script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script><![endif]-->
    </head>

    <body>
        <div class="container">
            <div class="hero-unit">
                <h1>Simple PHP App</h1>
                <?php
                    $instance_id = file_get_contents("http://169.254.169.254/latest/meta-data/instance-id");
                    $instance_type = file_get_contents("http://169.254.169.254/latest/meta-data/instance-type");
                    $instance_az = file_get_contents("http://169.254.169.254/latest/meta-data/placement/availability-zone");
                    print "This page is served by: ";
                    print "<br>";
                    print "\tInstance ID: " . $instance_id;
                    print "<br>";
                    print "\tInstance Type: " . $instance_type;
                    print "<br>";
                    print "\tInstance AZ: " . $instance_az;
                    print "</br>";
                ?>
                <p>The server is running PHP version <?php echo phpversion(); ?>.</p>
            </div>
            <div class="hero-unit">
            <?php
            function monte_carlo_pi($n){
                $m=0;
                for($i=0;$i<$n;$i++){
                    $x = mt_rand() / mt_getrandmax();
                    $y = mt_rand() / mt_getrandmax();
                    if(pow($x, 2) + pow($y, 2) <= 1){
                        $m = $m +1;
                    }
                }
                return 4 * $m/$n;
            }
            print "Pi from 10000 interations: ";
            print monte_carlo_pi(10000);
            print "</br>";
            print "Pi from 1000000 interations: ";
            print monte_carlo_pi(1000000);
            print "</br>";
            ?>
            </div>
        </div>

        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
        <script src="assets/js/bootstrap.min.js"></script>
    </body>

</html>
