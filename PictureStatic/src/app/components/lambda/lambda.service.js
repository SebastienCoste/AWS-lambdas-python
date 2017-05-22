(function() {
	'use strict';

	angular
	.module('pictureStatic')
	.service('lambda', lambda);

	/** @ngInject */
	function lambda($http) {

	    
		 var getTec =  function(lambdaUrl) {
			 console.log("loading technos ...")
			 return $http.post(lambdaUrl,null).then(function(result){
				 console.log(" ... loaded");
	            return result.data;
	        });
	    };

	    return { getTec: getTec };
	    
	}

})();
