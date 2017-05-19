(function() {
  'use strict';

  angular
    .module('pictureStatic')
    .run(runBlock);

  /** @ngInject */
  function runBlock($log) {

    $log.debug('runBlock end');
  }

})();
