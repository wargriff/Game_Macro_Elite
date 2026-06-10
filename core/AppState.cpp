#include "AppState.h"

AppStateStore& AppStateStore::instance()
{
    static AppStateStore store;
    return store;
}
