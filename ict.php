
<?xml version="1.0" encoding="UTF-8"?>
<vxml version = "2.1" application="http://webhosting.voxeo.net/208150/www/root.vxml">
<catch event="end"> 
 <disconnect/> 
</catch>

<?php

function generateRandomString($length = 10) {
    $characters = '0123456789abcdef';
    $charactersLength = strlen($characters);
    $randomString = '';
    for ($i = 0; $i < $length; $i++) {
        $randomString .= $characters[rand(0, $charactersLength - 1)];
    }
    return $randomString;
}



function saveFile($filename, $dir){
	
	$fn = md5(date('Y-m-d H:i:s:u')).generateRandomString(10).".wav";
	$fpath=$dir.$fn;
	copy($filename, $fpath);
	return $fn;
}

$dbh=new PDO("mysql:host="."localhost".';dbname='."***", "***", "***",array(PDO::MYSQL_ATTR_INIT_COMMAND => "set names utf8"));
// $sth = $dbh->prepare("insert into data (info) values('222');");
// $sth->execute();
$dir="/home/judge/src/web/wavs/";
$vxml_dir = "http://webhosting.voxeo.net/208125/www";
if(count($_GET)>0) { // get
	if($_GET["type"]=="exchange"){
		$sth = $dbh->prepare("select id,seed1,seed2,address,reference from exchange_list where seed1=? and seed2=? limit ".$_GET["start_id"].",1;");
		$sth->execute([$_GET["seed2"], $_GET["seed1"]]);
		$result=$sth->fetchAll();
		if(count(res)==0){
			// TODO
			header("Location: http://47.100.193.194/wavs/".$result[0][4]);
		}elseif($_GET["address"]==1){
			header("Location: http://47.100.193.194/wavs/".$result[0][3]);
		}else{
			header("Location: http://47.100.193.194/wavs/".$result[0][4]);
		}
		exit();
		// http://47.100.193.194/ict.php?type=exchange&seed1=Cotton&seed2=Rice&start_id=0
	}elseif($_GET["type"]=="buy"){
		$sth = $dbh->prepare("select id,seed,weight,price,address,reference from sell_list where seed=? and weight>=? limit ".$_GET["start_id"].",1;");
		$sth->execute([$_GET["seed"], $_GET["weight"]]);
		$result=$sth->fetchAll();
		if(count(res)==0){
			// TODO
			header("Location: http://47.100.193.194/wavs/".$result[0][5]);
		}elseif($_GET["address"]==1){
			header("Location: http://47.100.193.194/wavs/".$result[0][4]);
		}else{
			header("Location: http://47.100.193.194/wavs/".$result[0][5]);
		}
		exit();
		// http://47.100.193.194/ict.php?type=buy&seed=Cotton&weight=33&start_id=0
	}elseif($_GET["type"]=="recommend"){
		$sth = $dbh->prepare("select id,seed,weight,price,address,reference from report_list where seed=? order by id desc limit 1;");
		$sth->execute([$_GET["seed"]]); // seed type = recommend or weekly_report in table report list.
		$result=$sth->fetchAll();
		if(count(res)==0){
			// TODO
			header("Location: http://47.100.193.194/wavs/".$result[0][5]);
		}else{
			header("Location: http://47.100.193.194/wavs/".$result[0][5]);
		}
	}
} elseif(count($_POST)>0){ // post
	$address_fn = NULL;
	$reference_fn = NULL;
	if(isset($_FILES['address'])){
		$address_fn = saveFile($_FILES['address']['tmp_name'], $dir);
	}
	if(isset($_FILES['reference'])){
		$reference_fn = saveFile($_FILES['reference']['tmp_name'], $dir);
	}

	if($_POST["type"]=="exchange"){
		$sth = $dbh->prepare("insert into exchange_list (seed1, seed2, address, reference) values(?,?,?,?);");
		$sth->execute([$_POST["seed1"], $_POST["seed2"], $address_fn, $reference_fn]);

		echo '<menu id="finish" scope="dialog" dtmf="true">'.
			'<prompt>'.
			'Your Add has been posted online'.
			'<break time="1000"/>'.
			'To Search for another offer, Press 1'.
			'<break time="1000"/>'.
			'To Finish, Press 2'.
			'</prompt>'.
			'<choice next="'.$vxml_dir.'/en_exchange.vxml"></choice>'.
			'<choice event="end"></choice>'.
			'</menu>';
	}elseif($_POST["type"]=="sell"){
		$sth = $dbh->prepare("insert into sell_list (seed, weight, price, address, reference) values(?,?,?,?,?);");
		$sth->execute([$_POST["seed"], $_POST["weight"], $_POST["price"], $address_fn, $reference_fn]);
		
		echo '<menu id="last" scope="dialog" dtmf="true">'.
			'<prompt>'.
			'Your Add has been posted online'.
			'<break time="1000"/>'.
			'To Enter another add, Press 1'.
			'<break time="1000"/>'.
			'To Finish, Press 2'.
			'</prompt>'.
			'<choice next="'.$vxml_dir.'/en_sell.vxml"></choice>'.
			'<choice event="end"></choice>'.
			'</menu>';

	}elseif($_POST["type"]=="report"){
		$sth = $dbh->prepare("insert into report_list (seed, weight, price, address, reference) values(?,?,?,?,?);");
		$sth->execute([$_POST["seed"], $_POST["weight"], $_POST["price"], $address_fn, $reference_fn]);

		echo '<menu id="last" scope="dialog" dtmf="true">
		<prompt>
		You already upload your report, thank you for your help
		<break time="500"/>
		To finish, Press 1
		</prompt>
		<choice event="end"></choice>
		</menu>';
	}
}else{		// no params debug only
	$sth = $dbh->prepare("select * from data;");
	$sth->execute();
	$result=$sth->fetchAll();
	foreach ($result as $row){
		echo $row[0]." ".$row[1]." ";
	}
}

//sell: seed weight price  // address reference
// buy: read from db;
// exchange: seed1 seed2 // reference
// report seed weight price  // reference

// post: sell, exchange, report
// get: buy, exchange, recommend

?>

</vxml>
