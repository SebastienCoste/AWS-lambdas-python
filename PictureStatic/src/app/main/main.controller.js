(function() {
  'use strict';

  angular
    .module('pictureStatic')
    .controller('MainController', MainController);

  /** @ngInject */
  function MainController($timeout, $http, webDevTec, toastr, lambda) {
    var vm = this;

    vm.awesomeThings = [];
    vm.lambdaThings = [];
    vm.classAnimation = '';
    vm.creationDate = 1495126333555;
    vm.showToastr = showToastr;
    vm.allLambdaUrl = [];
    
    console.log("loading lambda urls")
    $http.get("lambdaReport.json").then(function(result){
    	vm.report = result.data;	
    	vm.report.allLambdas.forEach(function(entry) {
    	    console.log(entry.name + ": " + entry.url);
    	    vm.allLambdaUrl[entry.name] = entry.url
    	});
	    activate($http);
    });
    	
    

    function activate($http) {
//      getWebDevTec();
      getLambda($http);
      $timeout(function() {
        vm.classAnimation = 'rubberBand';
      }, 4000);
    }

    function showToastr() {
      toastr.info('Fork <a href="https://github.com/Swiip/generator-gulp-angular" target="_blank"><b>generator-gulp-angular</b></a>');
      vm.classAnimation = '';
    }

//    function getWebDevTec() {
//      vm.awesomeThings = webDevTec.getTec();
//
//      angular.forEach(vm.awesomeThings, function(awesomeThing) {
//        awesomeThing.rank = Math.random();
//      });
//    }
    

    function getLambda($http) {

    	var myDataPromise = lambda.getTec(vm.allLambdaUrl); 
        myDataPromise.then(function(result) { 
        	vm.lambdaThings = result; 
        }); 

        angular.forEach(vm.lambdaThings, function(lambdaThing) {
        	lambdaThing.rank = Math.random();
        });
      }
  }
})();
