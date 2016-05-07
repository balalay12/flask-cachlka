angular
	.module('app', ['ui.router', 'ngResource', 'ngCookies', 'ui.bootstrap', 'chart.js'])
	.run(function($http, $cookies) {
		$http.defaults.headers.common['X-CSRFToken'] = csrftoken;
		$http.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
	})
	.config(function($interpolateProvider, $resourceProvider, $stateProvider, $urlRouterProvider) {
		
		$interpolateProvider.startSymbol('{$');
		$interpolateProvider.endSymbol('$}');

		$resourceProvider.defaults.stripTrailingSlashes = false;

		$urlRouterProvider.otherwise('/home/news');
		
		$stateProvider
			.state('home', {
				url: '/home',
				templateUrl: template_dirs + '/main/main.html',
				controller: 'mainCtrl as vm'
			})
			.state('home.news', {
				url: '/news',
				template: '<h1>Hello world</h1><p>no news today :(</p>'
			})
			.state('registration', {
				url: '/registration',
				templateUrl: template_dirs + '/registration/reg.html',
				controller: 'registrationCtrl as vm'
			});
//			.state('main.login', {
//				url: '/login',
//				templateUrl: template_dirs + '/login/login.html',
//				controller: 'loginCtrl as vm'
//			})
//			.state('main.logout', {
//				url: '/logout',
//				template: '<ui-view/>',
//				controller: 'logoutCtrl'
//			})
//			.state('main.diary', {
//				url: '/diary',
//				templateUrl: template_dirs + '/diary/diary.html',
//				controller: 'diaryCtrl as vm'
//			})
//			.state('main.day', {
//				url: '/day/:date',
//				templateUrl: template_dirs + '/view_day/view_day.html',
//				controller: 'viewDayCtrl as vm'
//			})
//			.state('main.profile', {
//				url: '/profile',
//				templateUrl: template_dirs + '/profile/profile.html',
//				controller: 'profileCtrl as vm'
//			});
	});