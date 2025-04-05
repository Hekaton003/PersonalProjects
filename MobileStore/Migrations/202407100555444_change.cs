namespace MobileStore.Migrations
{
    using System;
    using System.Data.Entity.Migrations;
    
    public partial class change : DbMigration
    {
        public override void Up()
        {
            DropForeignKey("dbo.Reviews", "Mobile_ID", "dbo.Mobiles");
            DropIndex("dbo.Reviews", new[] { "Mobile_ID" });
            DropColumn("dbo.Reviews", "ProductID");
            RenameColumn(table: "dbo.Reviews", name: "Mobile_ID", newName: "ProductID");
            AlterColumn("dbo.Reviews", "ProductID", c => c.Int(nullable: false));
            CreateIndex("dbo.Reviews", "ProductID");
            AddForeignKey("dbo.Reviews", "ProductID", "dbo.Mobiles", "ID", cascadeDelete: true);
        }
        
        public override void Down()
        {
            DropForeignKey("dbo.Reviews", "ProductID", "dbo.Mobiles");
            DropIndex("dbo.Reviews", new[] { "ProductID" });
            AlterColumn("dbo.Reviews", "ProductID", c => c.Int());
            RenameColumn(table: "dbo.Reviews", name: "ProductID", newName: "Mobile_ID");
            AddColumn("dbo.Reviews", "ProductID", c => c.Int(nullable: false));
            CreateIndex("dbo.Reviews", "Mobile_ID");
            AddForeignKey("dbo.Reviews", "Mobile_ID", "dbo.Mobiles", "ID");
        }
    }
}
