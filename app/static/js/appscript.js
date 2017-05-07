/*global angular*/
/*global localStorage */
var wishlistApp = angular.module('wishlistApp', ['ngRoute']);
wishlistApp.config(['$locationProvider', function($locationProvider) {
	$locationProvider.hashPrefix('');
}]);

wishlistApp.config(function ($httpProvider) {
	$httpProvider.interceptors.push('AuthInterceptor');
});

wishlistApp.config(['$locationProvider', function($locationProvider) {
	$locationProvider.hashPrefix('');
}]);

wishlistApp.config(function($routeProvider) {
	$routeProvider

	// route for the home page
	.when('/', {
		templateUrl : '/static/templates/home.html',
		controller  : 'mainController'
	})

	// route for the login page
    .when('/login', {
		templateUrl : '/static/templates/login.html',
		controller  : 'loginController'
	})
	
	// route for the wish page
	.when('/wish', {
		templateUrl : '/static/templates/wish.html',
		controller  : 'wishController'
	})
	
	// route for the register page
	.when('/register', {
		templateUrl : '/static/templates/register.html',
		controller  : 'registerController'
	})
	
	// route for the new wish page
	.when('/new-wish', {
		templateUrl : '/static/templates/new-wish.html',
		controller  : 'newWishController'
	})
	.when('/profile', {
		templateUrl : '/static/templates/profile.html',
		controller  : 'profileController'
	})
	.otherwise({
		templateUrl : '/static/templates/home.html',
		controller  : 'mainController'
	});
});

wishlistApp.constant('CONS', {
  url: 'https://boiling-eyrie-14983.herokuapp.com/api/users',
  secret: 'XCX17CHARLIE'
});

wishlistApp.factory('AuthInterceptor', function ($rootScope, $q, AUTH_EVENTS) {
	return {
		responseError: function (response) {
			$rootScope.$broadcast({
				401: AUTH_EVENTS.notAuthenticated,
			}[response.status], response);
			return $q.reject(response);
		}
	};
});


wishlistApp.controller('mainController', function($scope, $http, $location, $route, CONS) {
	$scope.token = window.localStorage.getItem(CONS.secret);
	
	var token = window.localStorage.getItem(CONS.secret);
	if(token){
		var data = {'key' : $scope.token};
		$http({
			method  : 'POST',
			url     : CONS.url + '/data',
			data    : data,
			headers : {'Content-Type': 'application/json'} 
		 })
		.then(function (success){
			if(success.data.message === 'null'){
				$scope.userdata = success.data.user;
				localStorage.userdata = JSON.stringify($scope.userdata);
			}
		},function (error){
			// console.log('Server');
		});
	}

	$scope.logout = function(){
		window.localStorage.removeItem(CONS.secret);
		localStorage.userdata = null;
		localStorage.wishes = null;
		$http({
			method  : 'GET',
			url     : CONS.url + '/logout'
		 })
		 .then(function (){
		 	window.location.reload();
		 });
	};
});

wishlistApp.controller('wishController', function($scope, $location, $http, CONS) {
	var token = window.localStorage.getItem(CONS.secret);
	if( !token ){
		$location.path('/login');	
		$location.replace();
	}
	
	$scope.userdata = JSON.parse(localStorage.userdata);
	
	var userid = $scope.userdata.userid;
	localStorage.wishes = localStorage.wishes ? localStorage.wishes : JSON.stringify([]);
	
	$scope.wishes = JSON.parse(localStorage.wishes);
	
	$http({
		method: 'GET',
		url: CONS.url + '/' + userid + '/wishlist'
	}).then( function (success){
		var data = success.data;
		if(data.message == 'EMPTY'){
			$scope.wishmsg = 'You have no wish at this moment. Create one now.';
		}
		else{
			localStorage.wishes = JSON.stringify(data.wishes);
			$scope.wishes = JSON.parse(localStorage.wishes);
		}
	}, function(error){
		
	});
	
	$scope.removeWish = function (index) {
		var temp = $scope.wishes[index];
		
		var url = CONS.url + '/' + temp.user + '/wishlist/' + temp.id;
		
		$http({
			method: 'DELETE',
			url: url
		}).then( function (success){
			// console.log(success.data.message);
			$scope.wishes.splice(index, 1);
    		localStorage.wishes = JSON.stringify($scope.wishes);
		}, function(error){
			// console.log(error.data.message);
		});
	};
});

wishlistApp.constant('AUTH_EVENTS', {
  notAuthenticated: 'auth-not-authenticated'
});


wishlistApp.controller('loginController', function($scope, $http, $location, $route, CONS) {
	$scope.user = {
		email : '',
		password : ''
	};
	var token = window.localStorage.getItem(CONS.secret);
	if(token){
		$location.path('/');
		$location.replace();
		$route.reload();
	}

	$scope.login = function(){
		if(window.localStorage.getItem(CONS.secret)){
			$scope.authkey = window.localStorage.getItem(CONS.secret);
			$location.path('/home');
			$location.replace();
			$route.reload();
		}
		else{
		
			if($scope.user.email && $scope.user.password){
				$scope.emailerror = "";
				$scope.passworderror = "";
				$scope.scmessage  = "";

				$http({
					method  : 'POST',
					url     : CONS.url + '/login',
					data    : $scope.user,
					headers : {'Content-Type': 'application/json'} 
				 })
				.then(function (success){
					if(success.data.message === 'null'){
						$scope.userdata = success.data.user;
						$scope.authkey = success.data.key;
						window.localStorage.setItem(CONS.secret, success.data.key);
						window.location.reload();
					}
					else if(success.data.message === 'Invalid User'){
						$scope.emailerror = "Sorry, We could not locate a user with that email address. Please try again.";
					}
					else{
						$scope.passworderror = "Invalid Password. Please try again.";
					}
				},function (error){
					// console.log('Server');
				});

			}
			else{
				if(!$scope.user.email){
					$scope.emailerror = "Email Required";
				}
				else{
					$scope.emailerror = "";
				}
				if(!$scope.user.password){
					$scope.passworderror = "Password Required";
				}
				else{
					$scope.passworderror = "";
				}
			}
		}
	};
});

wishlistApp.controller('newWishController', function($scope, $http, $location, CONS) {
	$scope.successmsg = "";
	$scope.errormsg = "";
	var token = window.localStorage.getItem(CONS.secret);
	if( !token ){
		$location.path('/login');	
		$location.replace();
		$scope.message = "Please login to continue.";
	}
	$scope.newWish = {
		'url' : '',
		'title' : '',
		'description': '',
		'key' : '',
		'userid' : '',
		'message' : 'none',
		'thumbnail': ''
	};
	
	var u_id = JSON.parse(localStorage.userdata).userid;
	$scope.newWish.userid = u_id;
	$scope.newWish.key = window.localStorage.getItem(CONS.secret);
	var url = CONS.url + '/' + u_id + '/wishlist';
	
	$scope.createWish = function () {
		$scope.findimg = !$scope.findimg;
		$scope.successmsg = "";
		$scope.errormsg = "";
		if($scope.newWish.url == '' || $scope.newWish.description == '' || $scope.newWish.title == ''){
			$scope.errormsg = "All fields required.";
			$scope.findimg = !$scope.findimg;
		}
		else{
			var imgdata = {
				'url' : $scope.newWish.url,
				'message' : 'GET',
				'key' : window.localStorage.getItem(CONS.secret)
			};
			
			
			$http({
		    	method: 'POST',
		    	url: url, 
		    	data: imgdata,
		    	headers: {'Content-Type': 'application/json'} 
		    	
		    }).then(function(success){
		    	if(success.data.error){
		    		$scope.findimg = !$scope.findimg;
		    		$scope.errormsg = "The URL is invalid. Please try again";
		    	}
		    	else{
		    		$scope.images = success.data.images;
		    	}
		    }, function(error){
		    	$scope.errormsg = "There was an error. Please try again";
		    	$scope.findimg = !$scope.findimg;
		    	// console.log('error');
		    });
		}
	};
	
	$scope.submitwish = function(index){
		$scope.successmsg = "";
		$scope.errormsg = "";
		$scope.newWish.thumbnail = $scope.images[index];
		$http({
			method: 'POST',
			url: url,
			data: $scope.newWish,
			headers: {'Content-Type': 'application/json'} 
		}).then(function(success){
			$scope.successmsg = "Added successfully";
			$scope.newWish = {
				'url' : '',
				'title' : '',
				'description': '',
				'key' : '',
				'userid' : '',
				'message' : 'none',
				'thumbnail': ''
			};
			$scope.findimg = !$scope.findimg;
			$scope.images = null;
		}, function(error){
			$scope.errormsg = "There was an error. Please log out and try again";
		});
	};
	
	$scope.cancel = function(){
		$scope.images = null;
		$scope.findimg = false;
		$scope.successmsg = "";
		$scope.errormsg = "";
		$scope.newWish = {};
	};
});

wishlistApp.controller('registerController', function($scope, $location, $http, CONS, $route) {
	var token = window.localStorage.getItem(CONS.secret);
	if(token){
		$location.path('/');
		$location.replace();
		$route.reload();
	}
	
	var url = CONS.url + '/register';
	$scope.newProfile = function(){
		$scope.formmessage = [];
		if(!$scope.newuser){
			$scope.formmessage.push("Please fill in all fields");
		}
		else{
			if($scope.newuser.firstname == '' || $scope.newuser.lastname == '' || $scope.newuser.email == '' || $scope.newuser.password == '' || $scope.newuser.conpassword == ''){
				
				if($scope.newuser.firstname == ''){
					$scope.formmessage.push('First Name Required');
				}
				if($scope.newuser.lastname == ''){
					$scope.formmessage.push('Last Name Required');
				}
				if($scope.newuser.email == ''){
					$scope.formmessage.push('Email Required');
				}
				if($scope.newuser.password == '' || $scope.newuser.conpassword == ''){
					$scope.formmessage.push('Password required');
				}
			}
			else if(!$scope.newuser.firstname || !$scope.newuser.lastname || !$scope.newuser.email || !$scope.newuser.password || !$scope.newuser.conpassword){
				if(!$scope.newuser.firstname){
					$scope.formmessage.push('First Name Required');
				}
				if(!$scope.newuser.lastname){
					$scope.formmessage.push('Last Name Required');
				}
				if(!$scope.newuser.email){
					$scope.formmessage.push('Email Required');
				}
				if(!$scope.newuser.password || !$scope.newuser.conpassword){
					$scope.formmessage.push('Password required');
				}
			}
			else{
				
				if( !($scope.newuser.password == $scope.newuser.conpassword) ){
					$scope.formmessage.push('Passwords didn\'t match. Please try again.');
				}
				else{
					$http({
						method : 'POST', 
						url: url, 
						data: $scope.newuser, 
						headers : {'Content-Type': 'application/json'}
					}).then(function(success){
						var data = success.data;
						
						if(data.message == '200-OK'){
							if(data.error == 'null'){
								$location.path('/login');
								$location.replace();
								$route.reload();
							}
							else if(data.error == 'INCORRECT PASSWORDS'){
								$scope.formmessage.push('Passwords didn\'t match. Please try again.');
							}
							else if(data.error == 'USER EXIST'){
								$scope.formmessage.push('Email is already in use. Please try a different email address or proceed to login');
							}
							else {
								$scope.formmessage.push('Error Code: 0x09AFACBE');
							}
						}
					}, function(error){
						$scope.formmessage.push('There was an error. Please Refresh and try again');
					});
				}
				
			}
		}
	};
	
	$scope.cancel = function(){
		$scope.newuser = {};
	};
});

wishlistApp.controller('profileController', function($scope, $location, $http, CONS) {
	

	// $scope.userdata = null;
	// if(window.localStorage.getItem(LOCAL_TOKEN_KEY)){
	// 	$scope.token = window.localStorage.getItem(LOCAL_TOKEN_KEY);
	// 	// console.log($scope.token);
	// 	var data = {'key' : $scope.token};
	// 	$http({
	// 		method  : 'POST',
	// 		url     : 'http://info3180-project2-damainrussel.c9users.io:8081/api/users/data',
	// 		data    : data,
	// 		headers : {'Content-Type': 'application/json'} 
	// 	 })
	// 	.then(function (success){
	// 		if(success.data.message === 'null'){
	// 			// {'userid' : current_user.id, 'email' : user.username, 'firstname' : user.first_name, 'lastname' : user.last_name, 'image' : user.profile_photo}
	// 			$scope.userdata = success.data.user;
	// 			$scope.authkey = success.data.key;
	// 		}
	// 	},function (error){
	// 		console.log('Server');
	// 	});
	// }
});