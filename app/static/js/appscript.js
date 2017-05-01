/*global angular*/
/*global jQuery */
// create the module and name it scotchApp
var wishlistApp = angular.module('wishlistApp', ['ngRoute']);
// configure our routes


// =========================================================================================================

wishlistApp.constant('AUTH_EVENTS', {
  notAuthenticated: 'auth-not-authenticated'
});

wishlistApp.config(['$locationProvider', function($locationProvider) {
	$locationProvider.hashPrefix('');
}]);

wishlistApp.constant('API_ENDPOINT', {
  url: 'http://info3180-project2-damainrussel.c9users.io:8081/api'
  
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


// ===========================================================================================================
wishlistApp.config(function ($httpProvider) {
	$httpProvider.interceptors.push('AuthInterceptor');
});

// ======================================================================================================================







wishlistApp.config(['$locationProvider', function($locationProvider) {
	$locationProvider.hashPrefix('');
}]);
wishlistApp.config(function($routeProvider) {
	$routeProvider

	// route for the home page
	.when('/', {
		templateUrl : 'app/templates/home.html',
		controller  : 'mainController'
	})

	// route for the about page
	.when('/about', {
		templateUrl : 'app/templates/about.html',
		controller  : 'aboutController'
	})

	// route for the login page
    .when('/login', {
		templateUrl : '/app/templates/login.html',
		controller  : 'loginController'
	})
	
	// route for the logout page
	 .when('/logout',{
	     templateUrl : 'app/templates/logout.html',
	     controller: 'logoutController'
	 })
	
	// route for the wish page
	.when('/wish', {
		templateUrl : 'app/templates/wish.html',
		controller  : 'wishController'
	})
	
	// route for the register page
	.when('/register', {
		templateUrl : 'app/templates/register.html',
		controller  : 'registerController'
	})
	
	// route for the new wish page
	.when('/new-wish', {
		templateUrl : 'app/templates/new-wish.html',
		controller  : 'newWishController'
	});
});

// create the controller and inject Angular's $scope
wishlistApp.controller('mainController', function($scope) {
	$scope.message = 'Everyone come and see how good I look!';
});

wishlistApp.controller('wishController', function($scope) {
	$scope.message = 'Look! I am an wish page.';
});

wishlistApp.controller('loginController', function($scope, $http) {
	$scope.user = {
		email : '',
		password : ''
	};
	$scope.authentecated = false; 
	$scope.authToken= null;
	$scope.login = function(){
		// $scope.userEmail = 'hello world';
		if($scope.user.email && $scope.user.password){
			$scope.emailerror = "";
			$scope.passworderror = "";
			$scope.scmessage  = "";
			
			// $http({
			// 	method  : 'POST',
			// 	url     : 'http://info3180-project2-damainrussel.c9users.io:8081/api/user/login',
			// 	data    : $scope.user,
			// 	headers : {'Content-Type': 'application/json'} 
			// })
			// .then(function (success){
			// 	if(success.data.message === 'SUCCESS'){
			// 		$scope.data.userdata = success.user;
			// 		$scope.data.authkey = success.key;
			// 	}
			// 	$scope.scmessage = success.data.message;
			// 	console.log(success.data);
			// },function (error){
			// 	console.log('Server');
			// });
			// 	.success(function(data) {
			// 		$scope.scmessage = data.message;
			// 		// if (data.errors) {
			// 		// 	// Showing errors.
			// 		// 	$scope.errorName = data.errors.name;
			// 		// 	$scope.errorUserName = data.errors.username;
			// 		// 	$scope.errorEmail = data.errors.email;
			// 		// } else {
			// 		// 	$scope.message = data.message;
			// 		// }
			// });
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
	};
});

wishlistApp.controller('newWishController', function($scope) {
	// $scope.message = 'Contact us! JK. This is just a demo.';
	$scope.wishURL = 'login.com/wish.html';
	$scope.createWish = function () {
	    $scope.wishURL = 'url changed';
	};
});

wishlistApp.controller('registerController', function($scope) {
	$scope.message = 'Contact us! JK. This is just a demo.';
});

wishlistApp.controller('logoutController', function($scope) {
	$scope.message = 'Logout succesfully.';
});