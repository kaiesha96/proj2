/*global angular*/
var app = angular.module("myShoppingList", []); 
app.controller("myCtrl", function($scope, $http) {
    $scope.products = ["Milk", "Bread", "Cheese"];
    $scope.brand = 'Brand';
    $scope.addItem = function () {
        $scope.errortext = "";
        
        if (!$scope.addMe) {return;}
        if ($scope.products.indexOf($scope.addMe) == -1) {
            $scope.products.push($scope.addMe);
        } else {
            $scope.errortext = "The item is already in your shopping list.";
        }
    }
    $scope.removeItem = function (x) {
        $scope.errortext = "";    
        $scope.products.splice(x, 1);
    };
    $http.get("https://info3180-project2-damainrussel.c9users.io:8081/api/test")
        .then(function(response) {
            $scope.myWelcome = response.data;
            console.log(response.data);
        });
    $scope.isExists = function(item){
        return true;
    };
});

https://www.youtube.com/watch?v=H2xPKz3Uqu4
https://www.youtube.com/watch?v=aL95O4ruun0
https://www.youtube.com/watch?v=vs-egO-odAg
https://docs.angularjs.org/api/ng/directive/ngModel
https://scotch.io/tutorials/single-page-apps-with-angularjs-routing-and-templating
https://docs.angularjs.org/api/ng/service/$http#post
https://www.codecademy.com/courses/learn-angularjs/lessons/your-first-app/exercises/your-first-app-ng-click-i?action=lesson_resume
https://angularjs.org/