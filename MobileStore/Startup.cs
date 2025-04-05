using Microsoft.Owin;
using Owin;

[assembly: OwinStartupAttribute(typeof(MobileStore.Startup))]
namespace MobileStore
{
    public partial class Startup
    {
        public void Configuration(IAppBuilder app)
        {
            ConfigureAuth(app);
        }
    }
}
