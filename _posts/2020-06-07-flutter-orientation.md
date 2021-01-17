---
layout: post
title: "Controlling screen orientation in Flutter apps on a per-screen basis"
description: "A solution to a commonly needed feature for mobile apps made with Flutter."
image: /assets/blog-images/2020-06-07-cover.png
tags: ["Programming", "Flutter", "Dart"]
---

# Controlling screen orientation in Flutter apps on a per-screen basis

While working on the new Flutter app, I needed to make some screens appear in portrait mode only, others in landscape mode, and some should have supported both orientations. I had never done it before; all my previous apps were in portrait mode.

After quick googling, I’ve found the `SystemChrome` class and [this question on StackOverflow](https://stackoverflow.com/questions/50322054/flutter-how-to-set-and-lock-screen-orientation-on-demand). The mixins from StackOverflow answer work great until you begin to use `Navigator`. When you push new screens to the navigation stack, everything is fine, but when you pop, the orientation settings of the previous screen are not restored. There’s no lifecycle function like `viewWillAppear` in Flutter, and that screen doesn’t get any updates from the engine. I could have used a `Future` returned from `Navigator.push`, but the code would become ugly. Keeping track of all places where I need to update orientation settings is a bad idea. I needed a simple and elegant solution with as little overhead as possible.

I started developing my solution by asking myself two questions: “How can I know when the new screen goes to the stack?” and “How can I know when the screen leaves the stack?” The answer was simple: use `NavigatorObserver`. You can add multiple observers to any `Navigator`, including the one created by `MaterialApp`.

Let’s begin with writing the function which sets the screen orientation:

```dart
enum ScreenOrientation {
  portraitOnly,
  landscapeOnly,
  rotating,
}

void _setOrientation(ScreenOrientation orientation) {
  List<DeviceOrientation> orientations;
  switch (orientation) {
    case ScreenOrientation.portraitOnly:
      orientations = [
        DeviceOrientation.portraitUp,
      ];
      break;
    case ScreenOrientation.landscapeOnly:
      orientations = [
        DeviceOrientation.landscapeLeft,
        DeviceOrientation.landscapeRight,
      ];
      break;
    case ScreenOrientation.rotating:
      orientations = [
        DeviceOrientation.portraitUp,
        DeviceOrientation.landscapeLeft,
        DeviceOrientation.landscapeRight,
      ];
      break;
  }
  SystemChrome.setPreferredOrientations(orientations);
}
```

To make this function simpler to use, I defined an `enum` with possible orientation options. You can add more options if needed. You may also want to add `DeviceOrientation.portraitDown` for `ScreenOrientation.portraitOnly` if your app is targeted to tablets too. Another reason to use your own `enum` is to add an abstraction level. If Flutter gets another way to handle screen orientations, you only need to change the `_setOrientation` function.

The next step is to create a reusable `NavigatorObserver` subclass:

```dart
class NavigatorObserverWithOrientation extends NavigatorObserver {
  @override
  void didPop(Route route, Route previousRoute) {
    if (previousRoute.settings.arguments is ScreenOrientation) {
      _setOrientation(previousRoute.settings.arguments);
    } else {
      // Portrait-only is the default option
      _setOrientation(ScreenOrientation.portraitOnly);
    }
  }

  @override
  void didPush(Route route, Route previousRoute) {
    if (route.settings.arguments is ScreenOrientation) {
      _setOrientation(route.settings.arguments);
    } else {
      _setOrientation(ScreenOrientation.portraitOnly);
    }
  }
}
```

I’m using the `arguments` field of the `RouteSettings` class to store screen orientation settings. Don’t worry; you still can pass arguments to routes. If there are no arguments, or the type of `arguments` field is not `ScreenOrientation`, functions use the default option. In this example, it’s portrait-only, but you may change it.

Okay, now everything is ready to build the app:

```dart
class AppRoutes {
  static final home = "/";
  static final portrait = "/portrait";
  static final landscape = "/landscape";
  static final rotating = "/rotating";
}

RouteSettings rotationSettings(RouteSettings settings, ScreenOrientation rotation) {
  return RouteSettings(name: settings.name, arguments: rotation);
}

class MyApp extends StatelessWidget {
  final _observer = NavigatorObserverWithOrientation();

  Route<dynamic> _onGenerateRoute(RouteSettings settings) {
    if (settings.name == AppRoutes.home) {
      return MaterialPageRoute(builder: (context) => HomeScreen());
    } else if (settings.name == AppRoutes.portrait) {
      return MaterialPageRoute(builder: (context) => PortraitScreen());
    } else if (settings.name == AppRoutes.landscape) {
      return MaterialPageRoute(
        builder: (context) => LandscapeScreen(),
        settings: rotationSettings(settings, ScreenOrientation.landscapeOnly),
      );
    } else if (settings.name == AppRoutes.rotating) {
      return MaterialPageRoute(
        builder: (context) => RotatingScreen(),
        settings: rotationSettings(settings, ScreenOrientation.rotating),
      );
    }
    return null;
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Orientation Demo',
      theme: ThemeData(primarySwatch: Colors.blue,),
      onGenerateRoute: _onGenerateRoute,
      navigatorObservers: [_observer],
    );
  }
}
```

I don’t like hardcoded values, so I always define constants for app routes. `rotationSettings` is a little convenience function, it simplifies creating a `RouteSettings` object with `arguments` field set to rotation option. You may use the `arguments` field of the settings object passed to `_onGenerateRoute` to configure your widgets. I prefer to do it this way, instead of using `ModalRoute.of(context).settings.arguments` in the widget. However, if you’re not like me, you still can use my solution, but you will need to adapt code a bit:

1. Create a generic class for route arguments, which will have two fields: screen orientation and a generic field for route arguments.
2. Change `didPop` and `didPush` methods to check for the object of this class in the `arguments` field and then use the screen orientation field for `_setOrientation` call.

I’m not including the code of `HomeScreen`, `PortraitScreen`, `LandscapeScreen`, and `RotatingScreen`, because there’s no code related to the screen orientation. Everything is localized in `_onGenerateRoute` function. You can find the full demo app in [GitHub repository](https://github.com/Megus/flutter_orientation_demo).

My solution is not perfect because the screen rotation starts at the same time as route transition, which may lead to some undesired effects, but it’s good enough and worked for my app. I hope it will help some of you too. If you found a better way to implement a per-screen orientation control in Flutter, I’ll be happy to know it!

---

This article was originally published in [Flutter Community](https://medium.com/flutter-community/controlling-screen-orientation-in-flutter-apps-on-a-per-screen-basis-d637702f9368) on Medium.