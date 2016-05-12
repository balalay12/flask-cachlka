(function() {

  "use strict";

  angular
    .module("app")
    .controller("bodySizeCtrl", function($scope, $rootScope, $filter, $uibModalInstance, bodySizeFactory) {

      $scope.bodySize = {};

      if(!$rootScope.bodySizeId) {
        $scope.title = "Добавить замеры тела";
        $scope.adding = true;
      } else {
        $scope.title = "Изменить замеры тела";
        $scope.adding = false;

        bodySizeFactory.bodySize()
          .get({id: $rootScope.bodySizeId}, function(data) {
            $scope.bodySize = data.body_size;
            $scope.bodySize.date = new Date($scope.bodySize.date);
          });
      }

      $scope.cancel = function() {
        $rootScope.bodySizeId = null;
        $uibModalInstance.dismiss("cancel");
      }

      $scope.submit = function() {
        $scope.bodySize.date = $filter("date")($scope.bodySize.date, "yyyy-MM-dd");
        bodySizeFactory.bodySize()
          .save($scope.bodySize, function() {
            $rootScope.$broadcast("bodySizeEdited");
            $scope.cancel();
          },
          function(error) {
            $scope.error = error.data.error;
          })
      }

      $scope.update = function() {
        $scope.bodySize.date = $filter("date")($scope.bodySize.date, "yyyy-MM-dd");
        bodySizeFactory.bodySize()
          .update({id:$scope.bodySize.id}, $scope.bodySize, function() {
            $rootScope.$broadcast("bodySizeEdited");
            $scope.cancel();
          },
          function(error) {
            $scope.error = error.data.error;
          })
      }

      $scope.delete = function() {
        bodySizeFactory.bodySize()
          .delete({id: $rootScope.bodySizeId}, function() {
            $rootScope.$broadcast("bodySizeEdited");
            $scope.cancel();
          },
          function(error) {
            $scope.error = error.data.error;
          });
      }


      // calendar
      $scope.today = function() {
        $scope.bodySize.date = new Date();
      };
      $scope.today();

      $scope.clear = function() {
        $scope.bodySize.date = null;
      };

      $scope.inlineOptions = {
        customClass: getDayClass,
        minDate: new Date(),
        showWeeks: true
      };

      $scope.dateOptions = {
        // dateDisabled: disabled,
        formatYear: 'yy',
        maxDate: new Date(2020, 5, 22),
        minDate: new Date(),
        startingDay: 1
      };

      // Disable weekend selection
      function disabled(data) {
        var date = data.date,
        mode = data.mode;
        return mode === 'day' && (date.getDay() === 0 || date.getDay() === 6);
      }

      $scope.toggleMin = function() {
        $scope.inlineOptions.minDate = $scope.inlineOptions.minDate ? null : new Date();
        $scope.dateOptions.minDate = $scope.inlineOptions.minDate;
      };

      $scope.toggleMin();

      $scope.open = function() {
        $scope.popup.opened = true;
      };

      $scope.setDate = function(year, month, day) {
        $scope.bodySize.date = new Date(year, month, day);
      };

      $scope.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
      $scope.format = 'dd.MM.yyyy';
      $scope.altInputFormats = ['M!/d!/yyyy'];

      $scope.popup = {
        opened: false
      };

      var tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);
      var afterTomorrow = new Date();
      afterTomorrow.setDate(tomorrow.getDate() + 1);
      $scope.events = [
        {
          date: tomorrow,
          status: 'full'
        },
        {
          date: afterTomorrow,
          status: 'partially'
        }
      ];

      function getDayClass(data) {
        var date = data.date,
        mode = data.mode;
        if (mode === 'day') {
          var dayToCheck = new Date(date).setHours(0,0,0,0);

          for (var i = 0; i < $scope.events.length; i++) {
              var currentDay = new Date($scope.events[i].date).setHours(0,0,0,0);

            if (dayToCheck === currentDay) {
              return $scope.events[i].status;
            }
          }
        }

        return '';
      }
    });
})();