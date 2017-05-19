(function() {
	'use strict';

	angular
	.module('pictureStatic')
	.service('lambda', lambda);

	/** @ngInject */
	function lambda($http) {

	    
		 var getTec =  function(allLambdaUrl) {
			 console.log("loading technos ...")
			 return $http.post(allLambdaUrl["angular"],null).then(function(result){
				 console.log(" ... loaded");
	            return result.data;
	        });
	    };

	    return { getTec: getTec };
	    
	}

})();
