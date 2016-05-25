(function() {

	'use strict';

	angular
		.module('app')
		.controller('diaryCtrl', function($scope, $uibModal, $state, setsFactory) {

			var vm = this;
			vm.addDay = addDay;
			vm.monthIncrement = monthIncrement;
			vm.monthDecrement = monthDecrement;
			vm.viewDay = viewDay;

			var allSets = function() {
				setsFactory.getAllSets(function(data) {
						vm.sets = data.sets;
					});
			};
			allSets();

			$scope.$on('dayAdded', function() {
				allSets();
			});

			var getSetsByDate = function(_month, _year) {
				setsFactory.getAllSets({month:_month, year: _year}, function(data) {
					vm.sets = data.sets;
				});
			};

			var myDate = new Date();
			var month = myDate.getMonth() + 1;
			var year = myDate.getFullYear();

			function monthIncrement() {
				if(month >= 12) {
			        month = 1;
			        year = year + 1;
			        console.log(month, year);
			        getSetsByDate(month, year)
			    } else {
			        month = month + 1;
			        console.log(month, year);
			        getSetsByDate(month, year)
			    }
			}

			function monthDecrement() {
				if(month <= 1) {
			        month = 12;
			        year = year - 1;
			        console.log(month, year);
			        getSetsByDate(month, year)
			    } else {
			        month = month - 1;
			        console.log(month, year);
			        getSetsByDate(month, year)
		        }
			}

			function addDay() {
				var addDayModal = $uibModal.open({
					templateUrl: template_dirs + '/add_day/add_day.html',
					controller: 'addDayCtrl'
				})
			}

			function viewDay(_date) {
				$state.go('home.day', {
					date: _date
				});
			}
		});
})();